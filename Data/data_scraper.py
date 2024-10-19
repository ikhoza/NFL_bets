'''
Objective: Scrape data from https://www.sports-reference.com

Limits: 20 requests per minute. Currently sleeping is done to make sure each 
requests takes 3 seconds but this could be made more efficient.

An excessive amount of handshake failed errors are generated during scraping. 
This leads to a lot of logs in the command line; however, it does not seem to 
cause an issue with scraping.
'''

import os
import pandas as pd
from pathlib import Path
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import subprocess
import time
import winreg

parent_dir = Path(__file__).parent

# Initial setup
team_path = os.path.join(parent_dir, 'NFL_teams.csv')
teams = list(pd.read_csv(team_path, header=None)[0])
years = [str(i) for i in range(2010, 2024)]
# Get downloads folder - works for windows
sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
    source = winreg.QueryValueEx(key, downloads_guid)[0]

# Setup directories
default_filename = 'sportsref_download.xls'
source_file = os.path.join(source, default_filename)
temp_dest = os.path.join(parent_dir, 'temp')
final_dest = os.path.join(parent_dir, 'Files')

if not os.path.exists(temp_dest):
    os.mkdir(temp_dest)
if not os.path.exists(final_dest):
    os.mkdir(final_dest)

batch_file_path = os.path.join(parent_dir, 'xls_to_xlsx.bat')

# Make sure files download properly
if os.path.exists(source_file):
    os.remove(source_file)

def delete_popup():
    try:
        button_id = 'modal-close'
        button = driver.find_element(By.ID, button_id)
        button.click()
       
    except NoSuchElementException:
        pass

    except ElementNotInteractableException:
        pass


def get_games(driver, source_file, dest_file):
    while True:
        delete_popup()
            
        try:
            dropdown_css = '#all_games li.hasmore span'
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, dropdown_css))
            )

            firstLevelMenu = driver.find_element(By.CSS_SELECTOR, dropdown_css)
            driver.execute_script(
                "arguments[0].scrollIntoView(true);",
                firstLevelMenu
                )

            action = ActionChains(driver)
            action.move_to_element(firstLevelMenu).perform()
            
            button_css = '#all_games li.hasmore button.tooltip'
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, button_css))
            )
            buttons = driver.find_elements(By.CSS_SELECTOR, button_css)

            for button in buttons:
                if button.text == "Get as Excel Workbook":
                    button.click()
                    break
          
            
            # If file downloaded properly, move it
            if os.path.exists(source_file):
                os.replace(source_file, dest_file)
                break
        
        except ElementNotInteractableException:
            pass
        except TimeoutException:
            pass   
        except Exception as e:
            print(f"An error occurred: {e}")

# Set up WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

for team in teams:
    for year in years:
        team = team.lower()
        url = f'https://www.pro-football-reference.com/teams/{team}/{year}.htm'
        
        games_temp_dest = os.path.join(temp_dest, f'games_{team}_{year}.xls')
        games_final_dest = os.path.join(
            final_dest, f'games_{team}_{year}.xlsx'
            )
    
        # Check if file has been scraped incase script needs to be restarted
        if os.path.exists(games_temp_dest):
            continue
        
        driver.get(url)
        start = time.time()
        
        get_games(driver, source_file, games_temp_dest)
        
        # Makes sure no more than 20 requests/min received
        end = time.time()
        if end - start < 3:
            time.sleep(3 - (end - start)) 

# Close the WebDriver session when done
driver.quit()

try:
    print('Running xls_to_xlsx.bat')
    subprocess.run(batch_file_path, check=True, shell=True)
    print("Batch program executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error executing batch program: {e}")
    
# Clean up temp files
for file in os.listdir(temp_dest):
    os.remove(os.path.join(temp_dest, file))