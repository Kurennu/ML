import requests
from bs4 import BeautifulSoup
import time
import random

def get_unique_news_links(base_url, max_pages=5):
    unique_links = set()
    for page_num in range(1, max_pages + 1):
        page_url = f"{base_url}?page={page_num}"
        try:
            page = requests.get(page_url)
            page.raise_for_status()
            
            soup = BeautifulSoup(page.text, "html.parser")
            news_titles = soup.findAll('h3', class_='story-list__item-title')
            
            for data in news_titles:
                a_tag = data.find('a')
                if a_tag and a_tag.has_attr('href'):
                    full_link = f"https://www.newsvl.ru{a_tag['href']}"
                    unique_links.add(full_link)
            
            print(f"Страница {page_num}: найдено {len(news_titles)} новостей")
            time.sleep(random.uniform(0.5, 1.5))
        
        except Exception as e:
            print(f"Ошибка при парсинге страницы {page_num}: {e}")
    
    return list(unique_links)

def parse_news_page(link):
    try:
        news_page = requests.get(link)
        news_page.raise_for_status()
        
        news_soup = BeautifulSoup(news_page.text, "html.parser")
        story_text_div = news_soup.find('div', class_='story__text')
        story_text_title = news_soup.find('h1', class_='story__title')
        
        if story_text_title and story_text_div:
            title = story_text_title.text.strip()
            paragraphs = story_text_div.find_all('p')
            full_text = ' '.join(p.text.strip() for p in paragraphs)
            return f"{title}\n{full_text}\n{'=' * 50}\n"
        else:
            return f"Текст или заголовок новости не найден: {link}\n{'=' * 50}\n"
    
    except Exception as e:
        return f"Ошибка при парсинге {link}: {e}\n{'=' * 50}\n"

def main():
    base_url = 'https://www.newsvl.ru/'
    
    news_links = get_unique_news_links(base_url)
    print(f"Всего уникальных новостей: {len(news_links)}")
    
    newsData = []
    for link in news_links:
        print(f"Обрабатываю ссылку: {link}")
        news_content = parse_news_page(link)
        newsData.append(news_content)
        time.sleep(random.uniform(0.5, 1.5))
    
    with open('news.txt', 'w', encoding='utf-8') as f:
        f.writelines(newsData)
    
    print("Результаты записаны в файл news.txt")

if __name__ == "__main__":
    main()