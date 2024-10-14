import requests
import csv
from bs4 import BeautifulSoup
#from selenium import webdriver
#import pandas as pd
from urllib.request import urlopen
import re
from nltk.tokenize import RegexpTokenizer
import nltk
from urllib.parse import urlparse
import textstat

#driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

API_KEY = "dc30c420f094926af4ad37e1ca902b3b"

def make_api_request(query):

    API_URL = "https://api.semrush.com/?type=phrase_organic&key=dc30c420f094926af4ad37e1ca902b3b&phrase="+query+"&export_columns=Dn,Ur&database=us&display_limit=3"
    #print(API_URL)
    response = requests.get(API_URL)
    return response.text

def make_api_request2(query):

    API_URL2 = "https://api.semrush.com/?type=url_rank&key=dc30c420f094926af4ad37e1ca902b3b&export_columns=Or,Ot,Oc&url="+query+"&database=us"
    #print(API_URL2)
    response = requests.get(API_URL2)
    return response.text

def make_api_request3(query):

    API_URL3 = "https://api.semrush.com/analytics/v1/?key=dc30c420f094926af4ad37e1ca902b3b&type=backlinks_overview&target="+query+"&target_type=url&export_columns=ascore,domains_num"
    #https: // api.semrush.com / analytics / v1 /?key = YOUR_API_KEY & type = backlinks_overview & target = searchenginejournal.com & target_type = root_domain & export_columns = ascore, total, domains_num, urls_num, ips_num, ipclassc_num, follows_num, nofollows_num, sponsored_num, ugc_num, texts_num, images_num, forms_num, frames_num
    #print(API_URL3)
    response = requests.get(API_URL3)
    return response.text

def main():
    input_file = "input.csv"
    output_file = "output.csv"
    output_file2 = "output2.csv"
    output_file3 = "output3.csv"

    print("Starting Main")


    # Open file, export API output to rows, add headers
    file = open(input_file, 'r')
    csv_reader = csv.reader(file)
    ofile = open(output_file, "w", newline="")
    csv_writer = csv.writer(ofile)
    output_rows = []
    # output_headers = ["Keyword","Search Volume", "Keyword Difficulty", "CPC", "Keyword Intents","Domain","Ranking URL"]
    # output_rows.append(output_headers)
    temp_count = 0

    for row in csv_reader:
        #print(row[0])
        if row[0] == 'Keyword':
            print("first row")
        else:
            fquery = row[0]
            #print(fquery) #post-keyword cleaning
            api_response = make_api_request(fquery)
            #Completed raw 3 rows + headers

            #Cleaning Header Rows & New Lines Before Splitting To A List
            output_temp2 = api_response.replace("Domain;Url\r\n","")
            output_temp1 = output_temp2.replace("\r\n",";")

            #Changes to List
            output_temp = output_temp1.split(";")
            #print(output_temp) #after split function

            #insert keyword and extra metrics from input.csv
            output_temp.insert(0, row[8])
            output_temp.insert(0, row[5])
            output_temp.insert(0, row[4])
            output_temp.insert(0, row[3])
            output_temp.insert(0,fquery)
            #print(temp_count)
            #print(output_temp)
            temp_count = temp_count+1
            #writes each row to the output_rows array then when finished we'll write it to the output.csv
            output_rows.append(output_temp)

    # Print to output.csv
    output_rows_f = [bla for bla in output_rows if bla != []]
    #print(output_rows_f)
    csv_writer.writerows(output_rows_f)
    ofile.close()
    print("I've Finished Section 1")

# Starting New Section to Open the Output file to add Organic Cost/Traffic

    file2 = open('output.csv', 'r')
    csv_reader2 = csv.reader(file2)
    ofile2 = open(output_file2, "w", newline="")
    csv_writer2 = csv.writer(ofile2)

    csv_writer2 = csv.writer(ofile2)
    output_rows2 = []
    # from output1 == output_headers = ["Keyword","Search Volume", "Keyword Difficulty", "CPC", "Keyword Intents","Domain","Ranking URL"]
    output_headers2 = ["Keyword", "Search Volume", "Keyword Difficulty", "CPC", "Keyword Intents", "Domain", "Page URL","Organic Keywords", "Organic Traffic", "Organic Cost"]
    output_rows2.append(output_headers2)

    for row in csv_reader2:
        #print("Row 6:"+row[6])
        #print("Row 8:" + row[8])
        #print("Row 10:" + row[10])

        #First URL Call ********************************************************************************************************************************
        api_response2 = make_api_request2(row[6])
        #print(api_response2)
        #cleaning header rows and new lines
        output2_temp = api_response2.replace("Organic Keywords;Organic Traffic;Organic Cost\r\n","")
        #print(output2_temp)
        output_temp1 = output2_temp.replace("\r\n","")
        #print(output_temp1)

        #switch api response to a list
        output_temp = output_temp1.split(";")
        #print(output_temp)

        if output_temp == ['ERROR 50 :: NOTHING FOUND\n']:
            output_temp = ['0', '0', '0']
            #print(output_temp)
            output_temp.insert(0, row[6])
            output_temp.insert(0, row[5])
            output_temp.insert(0, row[4])
            output_temp.insert(0, row[3])
            output_temp.insert(0, row[2])
            output_temp.insert(0, row[1])
            output_temp.insert(0, row[0])
        else:
            #print(output_temp)
            output_temp.insert(0, row[6])
            output_temp.insert(0, row[5])
            output_temp.insert(0, row[4])
            output_temp.insert(0, row[3])
            output_temp.insert(0, row[2])
            output_temp.insert(0, row[1])
            output_temp.insert(0, row[0])

        output_rows2.append(output_temp)
        #print(output_temp)

        #Second URL Call ************************************************************************************************************************************
        api_response3 = make_api_request2(row[8])
        # cleaning header rows and new lines
        output2_temp = api_response3.replace("Organic Keywords;Organic Traffic;Organic Cost\r\n", "")
        # print(output2_temp)
        output_temp1 = output2_temp.replace("\r\n", "")
        # print(output_temp1)

        # switch api response to a list
        output_temp = output_temp1.split(";")

        if output_temp == ['ERROR 50 :: NOTHING FOUND\n']:
            output_temp = ['0', '0', '0']
            #print(output_temp)
            output_temp.insert(0, row[8])
            output_temp.insert(0, row[7])
            output_temp.insert(0, row[4])
            output_temp.insert(0, row[3])
            output_temp.insert(0, row[2])
            output_temp.insert(0, row[1])
            output_temp.insert(0, row[0])
        else:
            #print(output_temp)
            output_temp.insert(0, row[8])
            output_temp.insert(0, row[7])
            output_temp.insert(0, row[4])
            output_temp.insert(0, row[3])
            output_temp.insert(0, row[2])
            output_temp.insert(0, row[1])
            output_temp.insert(0, row[0])

        output_rows2.append(output_temp)


        # Third URL Call *************************************************************************************************************************************
        api_response4 = make_api_request2(row[10])
        # cleaning header rows and new lines
        output2_temp = api_response4.replace("Organic Keywords;Organic Traffic;Organic Cost\r\n", "")
        output_temp1 = output2_temp.replace("\r\n", "")
        # print(output_temp1)

        # switch api response to a list
        output_temp = output_temp1.split(";")

        if output_temp == ['ERROR 50 :: NOTHING FOUND\n']:
            output_temp = ['0', '0', '0']
            #print(output_temp)
            output_temp.insert(0, row[10])
            output_temp.insert(0, row[9])
            output_temp.insert(0, row[4])
            output_temp.insert(0, row[3])
            output_temp.insert(0, row[2])
            output_temp.insert(0, row[1])
            output_temp.insert(0, row[0])
        else:
            #print(output_temp)
            output_temp.insert(0, row[10])
            output_temp.insert(0, row[9])
            output_temp.insert(0, row[4])
            output_temp.insert(0, row[3])
            output_temp.insert(0, row[2])
            output_temp.insert(0, row[1])
            output_temp.insert(0, row[0])

        output_rows2.append(output_temp)

        #print(output_temp)

    # Print to CSV
    print("I've finished Section 2")
    csv_writer2.writerows(output_rows2)
    ofile2.close()

## Starting New Section to Open the Output file to add Linking Domains To Sheet


    file3 = open('output2.csv', 'r')
    csv_reader3 = csv.reader(file3)
    ofile3 = open(output_file3, "w", newline="")

    csv_writer3 = csv.writer(ofile3)
    output_rows3 = []
    output_headers3 = ["Keyword", "Search Volume", "Keyword Difficulty", "CPC", "Keyword Intents", "Domain", "Page URL","Organic Keywords", "Organic Traffic", "Organic Cost", "KOB Score","aScore","Linking Root Domains"]
    output_rows3.append(output_headers3)

    #Finding Length of csv_reader3
    #nI = sum(1 for row in csv_reader3)
    #print(nI) #shows how many rows are in csv_reader3

    #starting API Call Loop
    for row in csv_reader3:
        #print(row)
        if row[0] == 'Keyword':
            print("first row")
        else:
            api_response5 = make_api_request3(row[5])
            #print(api_response5) #Raw Response File
            #Cleaning Headers & Newlines
            output5_temp = api_response5.replace("ascore;domains_num\r\n", "")
            output5_temp_f = output5_temp.replace("\r\n", "")
            #switch api response to a list
            new_output = output5_temp_f.split(";")
            #Create new list based on current row then add on the 2 new metrics for aScore & Linking Root Domains
            print(f"This is where we break: {row[0]}")
            #print(f"This is the numerator: {row[9]}")
            #print(f"This is the demoninator: {row[2]}")
            kobScore = str(int(row[9]) / int(row[2]))
            new_output.insert(0, kobScore)
            new_output = row+new_output
            #print(new_output)
            #print(kobScore)

            output_rows3.append(new_output)


    csv_writer3.writerows(output_rows3)
    ofile3.close()

def uscrape():
    #create final file to add on url scrape data columns...
    output_file4 = "output4.csv"
    file4 = open('output3.csv', 'r')
    csv_reader3 = csv.reader(file4)
    ofile4 = open(output_file4, "w", newline="", encoding='utf-8')

    csv_writer4 = csv.writer(ofile4)
    output_rows4 = []
    output_headers4 = ["Keyword", "Search Volume", "Keyword Difficulty", "CPC", "Keyword Intents", "Domain", "Page URL",
                       "Organic Keywords", "Organic Traffic", "Organic Cost", "KOB Score", "aScore",
                       "Linking Root Domains", "Title", "Chars in Title", "H1 Tag", "# of H2 Tags", "H2 Tag(s)", "Meta Description", "# of Words Total", "# of Words in Body",
                       "# of Paragraphs in Body", "# of Internal Links", "# of External Links", "Flesch-Kincaid Grade Level"]
    output_rows4.append(output_headers4)

    # starting API Call Loop
    for row in csv_reader3:
        # print(row)
        if row[0] == 'Keyword':
            print("first row uscrape section")
        else:
            #print(f"URL Column 6: {row[6]}") column 6 (7-1) is where the actual URL exists
            # URL you want to scrape
            rowURL = row[6]
            kobURL = row[6]
            print(f"URL Being Scraped: {row[6]}")

            # Headers to mimic a browser visit
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://www.google.com/',
                'Upgrade-Insecure-Requests': '1',
            }

            # Fetch the content from the URL with headers
            response = requests.get(rowURL, headers=headers)
            print(f"Response Status Code: {response.status_code}")
            # Check if the request was successful
            if response.status_code == 200:
                # Parse the content with BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')

                # For example, to print the page title:
                #print(soup.title.text)
                try:
                    fTitle = soup.title.text
                except AttributeError:
                    fTitle = "No title found"

                # Find the title tag
                title_tag = soup.find('title')

                # Check if the title tag was found and get its text length
                if title_tag:
                    title_length = len(title_tag.text)
                    #print(f"Character length of the title tag: {title_length}")

                # finding H1 tag
                h1_tag = soup.find('h1')
                fh1_tag = "default"
                # Extract and print the text from the <h1> tag
                if h1_tag:
                    #print(f"H1 Tag: {h1_tag.text.strip()}")
                    fh1_tag = h1_tag.text.strip()
                else:
                    #print("No <h1> tag found.")
                    fh1_tag = "No <h1> tag found."

                # Find all <h2> tags
                h2_tags = soup.find_all('h2')

                # Count the number of <h2> tags
                h2_count = len(h2_tags)

                # Concatenate the text of each <h2> tag into one string
                concatenated_h2_texts = ' | '.join(h2.text.strip() for h2 in h2_tags)
                #print(concatenated_h2_texts)

                # Meta Description
                # Find the meta description tag
                meta_description_tag = soup.find('meta', attrs={'name': 'description'})

                # Check if the meta description tag was found
                if meta_description_tag and meta_description_tag.get('content'):
                    #print(f"Meta Description: {meta_description_tag['content']}")
                    fMetaDesc = meta_description_tag['content']
                else:
                    #print("Meta description not found.")
                    fMetaDesc ="Meta Description Not Found"

                # Extract all text from the soup object
                all_text = soup.get_text(separator=' ', strip=True)

                # Split the text into words based on whitespace and count them
                word_count = len(all_text.split())
                #print(f"Total word count from the page: {word_count}")


                # Find all <p> tags
                p_tags = soup.find_all('p')

                # Count the number of <p> tags
                num_paragraphs = len(p_tags)
                #print(f"Number of paragraphs on the page: {num_paragraphs}")

                # Words Within Paragraph Tags
                # Find all <p> tags
                p_tags = soup.find_all('p')

                # Initialize a word count
                total_word_count = 0

                # Loop through each paragraph and count the words
                for p in p_tags:
                    words = p.text.split()
                    total_word_count += len(words)

                #print(f"Total number of words in paragraphs: {total_word_count}")

                # Internal Links In Paragraphs
                # Find all <p> tags
                p_tags = soup.find_all('p')

                # Initialize an internal link count
                internal_links_count = 0

                # Extract the domain name from the original URL
                domain_name = urlparse(kobURL).netloc

                # Loop through each paragraph
                for p in p_tags:
                    # Find all <a> tags within the paragraph
                    a_tags = p.find_all('a')

                    # Check each link to see if it's internal
                    for a in a_tags:
                        link = a.get('href', '')

                        # Check if the link is internal
                        if link.startswith('/') or domain_name in link:
                            internal_links_count += 1

                #print(f"Total number of internal links in paragraphs: {internal_links_count}")

                # External Link Count
                # Find all <p> tags
                p_tags = soup.find_all('p')

                # Initialize an external link count
                external_links_count = 0

                # Extract the domain name from the original URL
                domain_name = urlparse(kobURL).netloc

                # Loop through each paragraph
                for p in p_tags:
                    # Find all <a> tags within the paragraph
                    a_tags = p.find_all('a')

                    # Check each link to see if it's external
                    for a in a_tags:
                        link = a.get('href', '')

                        # Check if the link is external
                        # Note: We're also excluding links that don't start with 'http' to filter out mailto: and javascript: links
                        if link.startswith('http') and domain_name not in link:
                            external_links_count += 1

                #print(f"Total number of external links in paragraphs: {external_links_count}")

                # Extract all text from the soup object
                all_text = soup.get_text(separator=' ', strip=True)

                # Calculate the Flesch-Kincaid Grade Level
                fk_grade_level = textstat.flesch_kincaid_grade(all_text)

                #print(f"Flesch-Kincaid Grade Level: {fk_grade_level}")

                output_test_row = [row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                                row[7], row[8], row[9], row[10], row[11],
                                row[12], fTitle, title_length, fh1_tag, h2_count, concatenated_h2_texts, fMetaDesc, word_count, total_word_count,
                                num_paragraphs, internal_links_count, external_links_count, fk_grade_level]
                output_rows4.append(output_test_row)

            else:
                print(f"Failed to retrieve the webpage, status code: {response.status_code}")


    #finish writing to file and closing file
    csv_writer4.writerows(output_rows4)
    ofile4.close()

if __name__ == "__main__":
    #main()
    uscrape()
