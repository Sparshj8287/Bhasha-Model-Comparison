import pandas as pd
import datetime
import json
from web_scraper import get_soup
from link_preprocessing import link_preprocessing
import hashlib
from link_preprocessing import main_part_of_url


def process_link(link):
    count = 0
    print("The scraped link is: ", link)
    trafik_text, links = get_soup(link)
    parsed_link = []

    for i in links:
        parsed_link.append(main_part_of_url(i))

    with open("Code_files/web_scraper_text/links.txt", "r", encoding="utf-8") as f:
        txt_links = f.read().splitlines()
        # print(txt_links)
        txt_parsed_links = [main_part_of_url(i) for i in txt_links]
        for index, i in enumerate(parsed_link):
            if i not in txt_parsed_links:
                txt_links.append(links[index])
                count += 1

        print(f"New general links found: {count}")
        link_text = "\n".join(i for i in txt_links)
        with open("Code_files/web_scraper_text/links.txt", "w", encoding="utf-8") as f:
            f.write(link_text)
    dt = datetime.datetime.now()
    dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    domain, india_gov = link_preprocessing(links)
    text_json = {
        "text": trafik_text,
        "source": "www.india.gov.in",
        "URL": link,
        "timestamp": dt_str,
    }
    # return (text_json, india_gov)
    return domain, text_json, india_gov


def domain_preprocessing(domains):
    domains_data = pd.read_csv("Code_files/web_scraper_text/domain.csv")
    domains_data_new = []
    for i in domains:
        if i not in domains_data["domain"].values:
            domains_data_new.append(i)
    count = len(domains_data_new)
    print(f"New domains found: {count}")
    new_data_df = pd.DataFrame(
        {"domain": domains_data_new, "values": [False] * len(domains_data_new)}
    )
    domains_data["values"] = domains_data["values"].astype(float)
    pd.concat([domains_data, new_data_df], ignore_index=True).to_csv(
        "Code_files/web_scraper_text/domain.csv", index=False
    )


def text_file_name(text):
    m = hashlib.sha256(text.encode("UTF-8"))
    return m.hexdigest()


def main():
    df = pd.read_csv(
        "/Users/ashujain/Desktop/web_scraper/Bhasha-Model-Comparison/Code_files/web_scraper_text/indic_gov_links.csv"
    )
    links_list = df["www.india.gov.in"].to_list()
    done_list = []
    undone_list = []
    for index, j in enumerate(links_list):
        try:
            second_count = 0
            df.loc[index, "values"] = True
            domain, text_json, india_gov = process_link(j)
            links_parsed_list = [main_part_of_url(i) for i in links_list]
            domain_preprocessing(domain)
            for i in india_gov["www.india.gov.in"]:
                parsed_link = main_part_of_url(i)
                if parsed_link not in links_parsed_list:
                    links_list.append(i)
                    second_count += 1
                    undone_list.append(i)

            done_list.append(j)
            done_list_text = "\n".join(i for i in done_list)
            undone_list_text = "\n".join(i for i in undone_list)

            with open("Code_files/web_scraper_text/done_links.txt", "a") as f:
                f.write(done_list_text)
            with open("Code_files/web_scraper_text/undone_links.txt", "a") as f:
                f.write(undone_list_text)

            df.to_csv("Code_files/web_scraper_text/indic_gov_links.csv", index=False)

            print(f"New india gov links found: {second_count}")
            print(
                "----------------------------------------------------------------------------------------------------"
            )
            print("\n\n\n\n")

            filename = text_file_name(text_json["text"])
            with open(
                f"Code_files/web_scraper_text/extracted_text/{filename}.json", "w"
            ) as f:
                json.dump(text_json, f, indent=4)

        except:
            pass


if __name__ == "__main__":
    main()
