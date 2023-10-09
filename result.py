from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import time
import pandas as pd
import os

print(pd.__version__)
# Read the roll numbers from inp.txt file
subjects = ['ISLAMIC EDUCATION', 'ENGLISH', 'URDU', 'BIOLOGY', 'PHYSICS', 'CHEMISTRY']
# Read the roll numbers from inp.txt file

with open('inp.txt', 'r') as f:
    roll_numbers = [line.strip() for line in f.readlines()]


with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
    driver.implicitly_wait(2) # seconds
   
    for roll_number in roll_numbers:
        try :
                print('roll number' , roll_number)
                output_df = pd.DataFrame(columns=['RollNumber', 'Name', 'FatherName'] + subjects + ['Total Marks'])
                driver.get("http://www.bisesargodha.edu.pk/content/boardresult.aspx")
                wait = WebDriverWait(driver, 5) # seconds

                exam_select = Select(wait.until(EC.presence_of_element_located((By.NAME, 'ctl00$ContentPlaceHolder1$DDLExam'))))
                exam_select.select_by_value('2')
                print('wao')
            
                year_select = Select(wait.until(EC.presence_of_element_located((By.NAME, 'ctl00$ContentPlaceHolder1$DDLExamYear'))))
                year_select.select_by_value('2022-2')
                print('yes')
             
                session_select = Select(wait.until(EC.presence_of_element_located((By.NAME, 'ctl00$ContentPlaceHolder1$DDLExamSession2'))))
                session_select.select_by_value('1')
                print('njdncj')
               
                # assuming your checkbox name is 'myCheckbox'
                checkbox_element = wait.until(EC.presence_of_element_located((By.NAME, 'ctl00$ContentPlaceHolder1$RbtSearchType')))
                checkbox_element.click()
                print('after checkbox')
                
                roll_number_input = wait.until(EC.presence_of_element_located((By.NAME, 'ctl00$ContentPlaceHolder1$TxtSearchText')))
                roll_number_input.send_keys(roll_number)
                print('after input')
              
                button = wait.until(EC.element_to_be_clickable((By.ID, 'ContentPlaceHolder1_BtnShowResults')))
                button.click()
                print('after btn')
               
                name = wait.until(EC.presence_of_element_located((By.ID, 'ContentPlaceHolder1_LblCandidateNameWithGrade'))).text
                father_name = wait.until(EC.presence_of_element_located((By.ID, 'ContentPlaceHolder1_LblFatherNameWithGrade'))).text
                
                print(f'Candidate Name: {name} \nFather Name: {father_name}')
                res = {'RollNumber': roll_number, 'Name': name, 'FatherName': father_name}
                total_marks = 0 
            
                j = 1
                for i in range(6): # Loop from 1 to 6
                    paper = wait.until(EC.presence_of_element_located((By.ID, f'ContentPlaceHolder1_LblPaper{j}WithGrade'))).text
                    paper_res = wait.until(EC.presence_of_element_located((By.ID, f'ContentPlaceHolder1_LblPaper{j}ObtainedMarksWithGrade'))).text
                    
                    print(f'Paper {j}: {paper} \nResult: {paper_res}\n')
                    res[subjects[i]] = paper_res
                    total_marks += int(paper_res)
                    j+=1
                res['Total Marks'] = total_marks 
                output_df = pd.concat([output_df, pd.DataFrame([res])]).reset_index(drop=True)
                # Check if 'output.csv' exists and if it is empty.
                if not os.path.isfile('output.csv') or os.stat('output.csv').st_size == 0:
                    # If 'output.csv' does not exist or if it is empty, write DataFrame with header.
                    output_df.to_csv('output.csv', index=False)
                else:
                    # If 'output.csv' exists and if it is not empty, append without writing the header.
                    output_df.to_csv('output.csv', mode='a', header=False, index=False)

        except Exception as e:
             print(f"Skipping roll number {roll_number} due to an error: {e}")
             continue

            
                


                
               