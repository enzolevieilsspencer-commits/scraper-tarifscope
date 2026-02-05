"""
Scraper 1: Récupération des informations d'un hôtel Booking.com
Usage: Appelé manuellement via API quand on ajoute un concurrent
"""
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeout
import re
import sys
import os
from typing import Optional, Dict, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.stealth_config import create_stealth_browser, close_browser, random_delay


def scrape_hotel_info(booking_url: str) -> Optional[Dict[str, Any]]:
    """
    Scrape les informations d'un hôtel depuis Booking.com
    
    Args:
        booking_url: URL complète de l'hôtel sur Booking.com
        
    Returns:
        Dict avec: name, location, address, stars, photoUrl
        None si erreur
    """
    print(f"🔍 Scraping infos pour: {booking_url}")
    
    browser, context, page = create_stealth_browser()
    
    try:
        # Aller sur la page de l'hôtel
        page.goto(booking_url, wait_until="domcontentloaded", timeout=30000)
        random_delay(2, 4)
        
        # Attendre que le contenu se charge
        page.wait_for_selector('h2[data-testid="title"]', timeout=15000)
        
        # Extraire les infos
        hotel_info = {
            "url": booking_url,
            "name": None,
            "location": None,
            "address": None,
            "stars": None,
            "photoUrl": None,
        }
        
        # Nom de l'hôtel
        try:
            name_element = page.locator('h2[data-testid="title"]').first
            hotel_info["name"] = name_element.inner_text().strip()
            print(f"  ✅ Nom: {hotel_info['name']}")
        except Exception as e:
            print(f"  ⚠️ Nom non trouvé: {e}")
        
        # Adresse
        try:
            address_element = page.locator('span[data-node_tt_id="location_score_tooltip"]').first
            hotel_info["address"] = address_element.inner_text().strip()
            print(f"  ✅ Adresse: {hotel_info['address']}")
        except:
            try:
                # Fallback: chercher dans les spans avec "Voir l'emplacement"
                address_element = page.locator('span:has-text("Voir sur la carte")').locator('..').first
                hotel_info["address"] = address_element.inner_text().replace("Voir sur la carte", "").strip()
                print(f"  ✅ Adresse (fallback): {hotel_info['address']}")
            except Exception as e:
                print(f"  ⚠️ Adresse non trouvée: {e}")
        
        # Location (ville)
        if hotel_info["address"]:
            # Extraire la ville depuis l'adresse
            parts = hotel_info["address"].split(",")
            if len(parts) >= 2:
                hotel_info["location"] = parts[-2].strip()
            else:
                hotel_info["location"] = "Saint-Rémy-de-Provence"  # Par défaut
        else:
            hotel_info["location"] = "Saint-Rémy-de-Provence"
        
        # Étoiles
        try:
            # Chercher les étoiles dans l'attribut aria-label
            stars_element = page.locator('[data-testid="rating-stars"]').first
            aria_label = stars_element.get_attribute("aria-label")
            
            if aria_label:
                # Extraire le nombre d'étoiles (ex: "4 étoiles" -> 4)
                match = re.search(r'(\d+)', aria_label)
                if match:
                    hotel_info["stars"] = int(match.group(1))
                    print(f"  ✅ Étoiles: {hotel_info['stars']}")
        except Exception as e:
            print(f"  ⚠️ Étoiles non trouvées: {e}")
        
        # Photo principale
        try:
            # Chercher l'image principale
            photo_element = page.locator('img[data-testid="main-image"]').first
            if not photo_element.count():
                photo_element = page.locator('img.bh-photo-grid-item').first
            
            photo_url = photo_element.get_attribute("src")
            if photo_url:
                hotel_info["photoUrl"] = photo_url
                print(f"  ✅ Photo récupérée")
        except Exception as e:
            print(f"  ⚠️ Photo non trouvée: {e}")
        
        print(f"✅ Scraping terminé pour {hotel_info['name']}")
        return hotel_info
        
    except PlaywrightTimeout:
        print(f"❌ Timeout lors du chargement de la page")
        return None
    except Exception as e:
        print(f"❌ Erreur lors du scraping: {e}")
        return None
    finally:
        close_browser(browser)


def test_scraper():
    """Fonction de test"""
    # URL de test (remplacer par une vraie URL)
    test_url = "https://www.booking.com/hotel/fr/chateau-de-roussan.fr.html"
    
    result = scrape_hotel_info(test_url)
    
    if result:
        print("\n📊 Résultat:")
        for key, value in result.items():
            print(f"  {key}: {value}")
    else:
        print("\n❌ Échec du scraping")


if __name__ == "__main__":
    test_scraper()
