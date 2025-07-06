import asyncio
import json
import os
import re
import time
import urllib.parse
from datetime import datetime

from api.controllers.product_controller import create_product
from playwright.async_api import async_playwright

AMAZON = "https://www.amazon.com.br/s?k="
OUTPUT_DIR = "resultados_amazon"
OUTPUT_DIR_TERA = "resultados_terabyte"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR_TERA, exist_ok=True)

banco_produtos_terabyte = []

produtos_terabyte = {
    "teclado": "perifericos/teclado",
    "mouse_gamer": "perifericos/mouse",
    "monitor": "monitores",
    "placa_de_video": "hardware/placas-de-video",
    "processador_intel_amd": "hardware/processadores",
}


async def scrape_terabyte(termo_pesquisa):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        )

        page = await context.new_page()

        try:
            print("🛒 Acessando Terabyte Shop...")
            await page.goto(
                f"https://www.terabyteshop.com.br/{termo_pesquisa}", timeout=60000
            )

            print("⏳ Aguardando carregamento dos produtos...")
            await page.wait_for_selector(".product-item__box", timeout=30000)

            print("🔄 Rolando página para carregar mais produtos...")
            await page.evaluate("""
                window.scrollTo(0, document.body.scrollHeight);
                setTimeout(() => window.scrollTo(0, 0), 500);
            """)
            await asyncio.sleep(2)

            print("🔍 Coletando dados dos produtos...")
            produtos = []
            items = await page.query_selector_all(".product-item__box")

            print(f"✅ Encontrados {len(items)} produtos na página inicial")

            for item in items:
                try:
                    nome_element = await item.query_selector(".product-item__name h2")
                    nome = await nome_element.inner_text() if nome_element else "N/A"

                    preco_element = await item.query_selector(
                        ".product-item__new-price span"
                    )
                    preco = await preco_element.inner_text() if preco_element else "N/A"

                    url_element = await item.query_selector("a.product-item__name")
                    url = (
                        await url_element.get_attribute("href")
                        if url_element
                        else "N/A"
                    )

                    sku = "N/A"
                    if url and "produto/" in url:
                        try:
                            sku = url.split("/produto/")[1].split("/")[0]
                        except:
                            pass

                    promo_element = await item.query_selector(".product-item__labels")
                    promocao = "Sim" if promo_element else "Não"

                    if url and not url.startswith("http"):
                        url = "https://www.terabyteshop.com.br" + url
                    if preco.strip() != "N/A":
                        produtos.append(
                            {
                                "sku": sku,
                                "nome": nome.strip(),
                                "preco": preco.strip(),
                                "url": url if url else "N/A",
                                "promocao": promocao,
                                "tipo_produto": termo_pesquisa,
                            }
                        )
                except Exception as e:
                    print(f"⚠️ Erro em um produto: {str(e)}")
                    continue

            banco_produtos_terabyte.extend(produtos)

            timestamp = time.strftime("%Y%m%d-%H%M%S")
            if "/" in termo_pesquisa:
                termo_pesquisa = termo_pesquisa.split("/")[1]
            filename = f"terabyte_produtos_{termo_pesquisa}.json"
            #  output_path = os.path.join(OUTPUT_DIR_TERA, filename)

            #    with open(output_path, "w", encoding="utf-8") as f:
            #       json.dump(produtos, f, ensure_ascii=False, indent=2)

            print(f"\n✅ Sucesso! {len(produtos)} produtos salvos em '{filename}'")

            return filename

        except Exception as e:
            print(f"\n❌ Erro durante scraping: {str(e)}")
            return None

        finally:
            await browser.close()


async def scrape_amazon(url: str):
    produtos = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        items = await page.query_selector_all("a.s-no-outline")

        for i, item in enumerate(items):
            href = await item.get_attribute("href")
            nome = await item.query_selector("img")
            nome_texto = await nome.get_attribute("alt") if nome else ""

            preco_span = await page.query_selector_all("span.a-price span.a-offscreen")
            nota_span = await page.query_selector_all("span.a-icon-alt")

            preco = await preco_span[i].inner_text() if i < len(preco_span) else ""
            nota = await nota_span[i].inner_text() if i < len(nota_span) else ""

            produtos.append(
                {
                    "url": "https://www.amazon.com.br" + href if href else "",
                    "name": nome_texto,
                    "price": preco,
                    "rating": nota[:3] if nota else "",
                }
            )

        await browser.close()
    return produtos


lista_produtos = [
    "teclado",
    "mouse_gamer",
    "monitor",
    "placa_de_video",
    "processador_intel_amd",
]


def montar_url(termo_pesquisa):
    return urllib.parse.quote(termo_pesquisa, safe="")


async def search():
    todos_amazon = []
    for termo in lista_produtos:
        for page_num in range(1, 11):
            url = f"{AMAZON}{montar_url(termo)}&page={page_num}"
            print(f"[+] Buscando: {url}")
            resultados = await scrape_amazon(url)
            if resultados:
                todos_amazon.extend(resultados)
            await asyncio.sleep(1)

        if todos_amazon:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"amazon_{termo}.json"
            #  path = os.path.join(OUTPUT_DIR, filename)
            # with open(path, "w", encoding="utf-8") as f:
            #    json.dump(todos_amazon, f, ensure_ascii=False, indent=2)
            print(f"✅ Amazon: {len(todos_amazon)} produtos salvos em {filename}")
            todos_amazon.clear()

        await scrape_terabyte(produtos_terabyte[termo])


async def get_product_details(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
        )
        page = await context.new_page()
        await page.goto(url, timeout=60_000)
        await page.wait_for_timeout(2000)

        # Remove popups
        try:
            await page.wait_for_selector("#bannerPop", timeout=5000)
            await page.evaluate("""
                () => {
                    const banner = document.getElementById('bannerPop');
                    if (banner) banner.remove();
                    document.querySelectorAll('.modal-backdrop, .fade.in').forEach(e => e.remove());
                }
            """)
        except:
            pass

        # Scroll e clicar em "Especificações Técnicas"
        try:
            await page.evaluate(
                "document.querySelector('a[href=\"#esptec\"]').scrollIntoView()"
            )
            await page.click('a[href="#esptec"]')
        except:
            pass

        try:
            await page.evaluate(
                "document.querySelector('a[href=\"#cg\"]').scrollIntoView()"
            )
            await page.click('a[href="#cg"]')
            await page.wait_for_selector("div#cg", state="visible", timeout=10000)
        except:
            pass

        # Descrição
        descricao = ""
        try:
            el = await page.query_selector("div.descricao section.bg_branco p")
            if el:
                descricao = await el.inner_text()
        except:
            pass

        if not descricao:
            try:
                el = await page.query_selector("div.descricao section.bg_preto p")
                if el:
                    descricao = await el.inner_text()
            except:
                pass

        if not descricao:
            try:
                el = await page.query_selector(
                    "div.descricao section.bg_preto div[style*='margin']"
                )
                if el:
                    textos = await page.eval_on_selector_all(
                        "div.descricao section.bg_preto div[style*='margin'] *",
                        "elements => elements.map(e => e.innerText).filter(Boolean).join(' ')",
                    )
                    descricao = textos
            except:
                pass

        # Specs
        specs_dict = {}
        try:
            await page.wait_for_selector("div.tecnicas", timeout=20000)
            p_tags = await page.query_selector_all("div.tecnicas > p")
            for ptag in p_tags:
                text = await ptag.inner_text()
                text = re.sub(r"\s+", " ", text).strip()
                if not text:
                    continue

                if ":" in text:
                    parts = text.split(":", 1)
                    key = parts[0].strip()
                    val = parts[1].strip().strip('"')
                    specs_dict[key] = val
                else:
                    specs_dict[text] = ""
        except:
            pass

        image_url = ""
        try:
            img_element = await page.query_selector("img.zoomImg")
            if img_element:
                image_url = await img_element.get_attribute("src")
        except:
            pass

        await browser.close()
        return descricao.strip(), specs_dict, image_url


async def search_details():
    if banco_produtos_terabyte:
        for produto in banco_produtos_terabyte:
            try:
                desc, esp, img = await get_product_details(produto["url"])
                produto["descricao"] = desc
                produto["tecnica"] = esp
                produto["imagem"] = img
                print(desc)
            except Exception as e:
                print(produto["url"])
                print(e)

    teclados = [
        p
        for p in banco_produtos_terabyte
        if p.get("tipo_produto") == "perifericos/teclado"
    ]
    processadores = [
        p
        for p in banco_produtos_terabyte
        if p.get("tipo_produto") == "hardware/processadores"
    ]
    mouse = [
        p
        for p in banco_produtos_terabyte
        if p.get("tipo_produto") == "perifericos/mouse"
    ]
    gpu = [
        p
        for p in banco_produtos_terabyte
        if p.get("tipo_produto") == "hardware/placas-de-video"
    ]
    monitores = [
        p for p in banco_produtos_terabyte if p.get("tipo_produto") == "monitores"
    ]
    print(teclados[0])
    print(processadores[0])
    print(mouse[0])
    print(monitores[0])
    print(gpu[0])


MAP_CATEGORIAS = {
    "perifericos/teclado": "keyboard",
    "perifericos/mouse": "mouse",
    "hardware/placas-de-video": "gpu",
    "hardware/processadores": "cpu",
    "monitores": "monitor",
}


def buscar_campo(tecnica, *possiveis_nomes):
    for nome in possiveis_nomes:
        if nome in tecnica:
            return tecnica[nome]
    return None


def salvar_produtos_django(produtos):
    for produto in produtos:
        tipo_scraping = produto.get("tipo_produto")
        categoria_django = MAP_CATEGORIAS.get(tipo_scraping)

        if not categoria_django:
            print(
                f"⚠️ Categoria não mapeada: {tipo_scraping}. Produto ignorado: {produto.get('nome')}"
            )
            continue

        tecnica = produto.get("tecnica", {})
        descricao = produto.get("descricao", "")
        preco_str = (
            produto.get("preco", "0")
            .replace("R$", "")
            .replace(".", "")
            .replace(",", ".")
            .strip()
        )

        try:
            preco_float = float(preco_str)
        except ValueError:
            preco_float = 0.0

        # Preparar spec_fields padrão
        spec_fields = {
            "model": buscar_campo(tecnica, "Modelo", "Model"),
            "store": "Terabyte Shop",
            "url": produto.get("url"),
            "available": True,
            "value": preco_float,
            "collection_date": datetime.now(),
        }

        match categoria_django:
            case "keyboard":
                spec_fields.update(
                    {
                        "key_type": buscar_campo(
                            tecnica, "Switch", "Tipo de switch", "Tipo de tecla"
                        ),
                        "layout": buscar_campo(
                            tecnica, "Nomeros de teclas", "Número de teclas", "Layout"
                        ),
                        "connectivity": buscar_campo(
                            tecnica, "Cabo", "Conectividade", "Tipo de conexão"
                        )
                        or "Fio",
                        "dimension": buscar_campo(
                            tecnica, "Tamanho do teclado", "Dimensão", "Tamanho"
                        ),
                    }
                )
            case "cpu":
                spec_fields.update(
                    {
                        "integrated_video": buscar_campo(
                            tecnica, "Vídeo Integrado", "Vídeo onboard", "GPU Integrada"
                        )
                        or "Não informado",
                        "socket": buscar_campo(tecnica, "Soquete", "Socket"),
                        "core_number": buscar_campo(
                            tecnica, "Núcleos de CPU", "Núcleos"
                        ),
                        "thread_number": buscar_campo(
                            tecnica, "Threads", "Número de threads"
                        ),
                        "frequency": buscar_campo(
                            tecnica, "Clock base", "Frequência base", "Clock"
                        ),
                        "mem_speed": buscar_campo(
                            tecnica, "Memória", "Velocidade Memória", "Velocidade RAM"
                        ),
                    }
                )
            case "gpu":
                spec_fields.update(
                    {
                        "vram": buscar_campo(
                            tecnica, "Memory Size", "Memória", "Capacidade de memória"
                        ),
                        "chipset": buscar_campo(tecnica, "Chipset", "Modelo", "GPU"),
                        "max_resolution": buscar_campo(
                            tecnica, "Digital max resolution", "Resolução Máxima"
                        ),
                        "output": buscar_campo(
                            tecnica, "Output", "Saídas", "Conectores", "Portas"
                        ),
                        "tech_support": buscar_campo(
                            tecnica, "DirectX", "OpenGL", "Tecnologias suportadas"
                        ),
                    }
                )
            case "mouse":
                spec_fields.update(
                    {
                        "brand": buscar_campo(tecnica, "Marca"),
                        "dpi": buscar_campo(tecnica, "DPI", "Resolução"),
                        "connectivity": buscar_campo(
                            tecnica, "Conectividade", "Cabo", "Tipo de conexão"
                        )
                        or "Fio",
                        "color": buscar_campo(tecnica, "Cor", "Cor predominante"),
                    }
                )
            case "monitor":
                spec_fields.update(
                    {
                        "inches": buscar_campo(
                            tecnica, "Tamanho da tela", "Polegadas", "Tamanho"
                        ),
                        "panel_type": buscar_campo(
                            tecnica, "Tipo de luz de fundo", "Painel", "Tipo Painel"
                        ),
                        "proportion": buscar_campo(
                            tecnica, "Proporção", "Aspect Ratio"
                        ),
                        "resolution": buscar_campo(
                            tecnica, "Resolução", "Resolução Máxima"
                        ),
                        "refresh_rate": buscar_campo(
                            tecnica,
                            "Taxa de atualização",
                            "Frequência",
                            "Taxa de contraste",
                        ),
                        "color_support": buscar_campo(
                            tecnica, "RGB", "Suporte a cores", "Cores"
                        ),
                        "output": buscar_campo(
                            tecnica, "Portas", "Conectores", "Entradas", "Saídas"
                        ),
                    }
                )
            case _:
                pass

        brand = buscar_campo(tecnica, "Marca")

        image_url = produto.get("image")

        try:
            create_product(
                name=produto.get("nome"),
                category=categoria_django,
                description=descricao,
                image_url=image_url,
                brand=brand,
                **spec_fields,
            )
            print(f"✅ Produto criado: {produto.get('nome')} [{categoria_django}]")

        except Exception as e:
            print(f"❌ Erro ao criar produto '{produto.get('nome')}': {str(e)}")


async def main():
    await search()
    print("buscar detalhes")
    await search_details()
    salvar_produtos_django(banco_produtos_terabyte)


if __name__ == "__main__":
    asyncio.run(main())
