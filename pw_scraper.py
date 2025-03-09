"""
Este código utiliza a biblioteca Playwright para automatizar 
a busca e o download de artigos científicos no site do arXiv.
"""
from urllib.request import urlretrieve
from playwright.sync_api import sync_playwright

# Abre o navegador
with sync_playwright() as pw:
    browser = pw.firefox.launch(headless=False)
    page = browser.new_page()
    page.goto("http://arxiv.org/search")

    # Preenche o formulário
    page.get_by_placeholder("Search term...").fill("neural network")
    page.get_by_role("button").get_by_text("Search").nth(1).click()

    # Espera pelos resultados carregarem
    page.wait_for_selector("xpath=//a[contains(@href, 'arxiv.org/pdf')]")

    # Obtém os elementos em vez de apenas localizadores
    links = page.locator(
        "xpath=//a[contains(@href, 'arxiv.org/pdf')]"
        ).element_handles()

    for link in links:
        url = link.get_attribute("href")
        urlretrieve(url, "data/" + url[-5:] + ".pdf")

    page.screenshot(path="screenshot.png")
    browser.close()
