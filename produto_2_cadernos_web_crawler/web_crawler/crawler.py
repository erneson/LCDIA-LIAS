import os
import time

import re
import glob
import simpledbf

import numpy as np
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from selenium.common.exceptions import TimeoutException

class element_attribute_is_changing(object):
    def __init__(self, locator, attribute):
        self.locator = locator
        self.attribute = attribute
    
    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        value = element.get_attribute(self.attribute)
        time.sleep(1)
        new_value = element.get_attribute(self.attribute)
        if value == new_value:
            return element
        else:
            return False

def FindTagValue(driver, xpath, tag):
    try:
        element = WebDriverWait(driver, 5).until(element_attribute_is_changing((By.XPATH, xpath), tag))
        tag_value = element.get_attribute(tag)
        return tag_value
    except TimeoutException:
        print('Error (FindTagValue): TimeoutException')

def FindTags(driver, xpath):
    try:
        elements = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        return elements
    except TimeoutException:
        print('Error (FindTags): TimeoutException')

def FindPatterns(isheadless, reverse = False):
    d = {'encoded': [],
         't00': [],
         't01': [],
         't10': [],
         't11': [],
         't20': [],
         't21': [],
         'label': []}
    
    if isheadless:
        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')

        driver = webdriver.Firefox(options = options)
    else:
        driver = webdriver.Firefox()
    
    try:
        url = 'https://datasus.saude.gov.br/transferencia-de-arquivos/'
        driver.get(url)
        
        select0_tag = driver.find_element(By.XPATH, '//select[@id="mySelect"]') # fonte
        option0_tags = FindTags(driver, '//select[@id="mySelect"]/child::option')
        
        if reverse:
            option0_tags = option0_tags[::-1]
        
        for option0_tag in option0_tags:
            t00 = option0_tag.get_attribute('value')
            t01 = option0_tag.get_attribute('innerText')
            select0_tag_form = Select(select0_tag)
            select0_tag_form.select_by_value(t00)
            
            select1_tag = driver.find_element(By.XPATH, '//select[@id="modSelect"]') # modalidade
            option1_tags = FindTags(driver, '//select[@id="modSelect"]/child::option')
            
            if reverse:
                option1_tags = option1_tags[::-1]

            for option1_tag in option1_tags:
                t10 = option1_tag.get_attribute('value')
                t11 = option1_tag.get_attribute('innerText')
                select1_tag_form = Select(select1_tag)
                select1_tag_form.select_by_value(t10)
                
                select2_tag = driver.find_element(By.XPATH, '//select[@id="tipo_arquivo"]') # tipo de dado
                option2_tags = FindTags(driver, '//select[@id="tipo_arquivo"]/child::option')
                
                if reverse:
                    option2_tags = option2_tags[::-1]
                
                for option2_tag in option2_tags:
                    t20 = option2_tag.get_attribute('value')
                    t21 = option2_tag.get_attribute('innerText')
                    select2_tag_form = Select(select2_tag)
                    select2_tag_form.select_by_value(t20)
                    
                    style3 = FindTagValue(driver, '//div[@id="linha_competencia"]', 'style') # ano
                    style5 = FindTagValue(driver, '//div[@id="linha_uf"]', 'style') # uf

                    if style3 == 'display: none;':
                        if style5 == 'display: none;':
                            ### Label 1 ###
                            t = [t00, t01, t10, t11, t20, t21]
                            d['encoded'].append('|'.join(t))
                            d['t00'].append(t00)
                            d['t01'].append(t01)
                            d['t10'].append(t10)
                            d['t11'].append(t11)
                            d['t20'].append(t20)
                            d['t21'].append(t21)
                            d['label'].append(1)
                            ### Label 1 ###
                        else:
                            ### Label 2 ###
                            t = [t00, t01, t10, t11, t20, t21]
                            d['encoded'].append('|'.join(t))
                            d['t00'].append(t00)
                            d['t01'].append(t01)
                            d['t10'].append(t10)
                            d['t11'].append(t11)
                            d['t20'].append(t20)
                            d['t21'].append(t21)
                            d['label'].append(2)
                            ### Label 2 ###e
                    else:
                        style4 = FindTagValue(driver, '//div[@id="box_mes"]', 'style') # mês

                        if style4 == 'display: none;':
                            if style5 == 'display: none;':
                                ### Label 3 ###
                                t = [t00, t01, t10, t11, t20, t21]
                                d['encoded'].append('|'.join(t))
                                d['t00'].append(t00)
                                d['t01'].append(t01)
                                d['t10'].append(t10)
                                d['t11'].append(t11)
                                d['t20'].append(t20)
                                d['t21'].append(t21)
                                d['label'].append(3)
                                ### Label 3 ###
                            else:
                                ### Label 4 ###
                                t = [t00, t01, t10, t11, t20, t21]
                                d['encoded'].append('|'.join(t))
                                d['t00'].append(t00)
                                d['t01'].append(t01)
                                d['t10'].append(t10)
                                d['t11'].append(t11)
                                d['t20'].append(t20)
                                d['t21'].append(t21)
                                d['label'].append(4)
                                ### Label 4 ###
                        else:
                            if style5 == 'display: none;':
                                ### Label 5 ###
                                t = [t00, t01, t10, t11, t20, t21]
                                d['encoded'].append('|'.join(t))
                                d['t00'].append(t00)
                                d['t01'].append(t01)
                                d['t10'].append(t10)
                                d['t11'].append(t11)
                                d['t20'].append(t20)
                                d['t21'].append(t21)
                                d['label'].append(5)
                                ### Label 5 ###
                            else:
                                ### Label 6 ###
                                t = [t00, t01, t10, t11, t20, t21]
                                d['encoded'].append('|'.join(t))
                                d['t00'].append(t00)
                                d['t01'].append(t01)
                                d['t10'].append(t10)
                                d['t11'].append(t11)
                                d['t20'].append(t20)
                                d['t21'].append(t21)
                                d['label'].append(6)
                                ### Label 6 ###
                    
                    select2_tag_form.deselect_by_value(t20)
                select1_tag_form.deselect_by_value(t10)
            select0_tag_form.deselect_by_value(t00)
        driver.quit()
    except:
        driver.quit()
    
    new_df = pd.DataFrame(d)
    os.makedirs('urls/', exist_ok = True)
    filename = 'urls/patterns.csv'
    if os.path.isfile(filename):
        old_df = pd.read_csv(filename,
                             sep = ';',
                             dtype = str,
                             encoding = 'utf-8')
        
        ### MERGE ###
        new_df = pd.merge(old_df,
                          new_df,
                          on = 'encoded',
                          how = 'outer',
                          suffixes = ('', '_y'))
        
        cols = ['t00',
                't01',
                't10',
                't11',
                't20',
                't21',
                'label']
        
        for col in cols:
            col_y = '{}_y'.format(col)
            new_df[col] = new_df[col].fillna(new_df[col_y])

        cols = ['encoded'] + cols
        new_df = new_df[cols]
        ### MERGE ###
    
    new_df.sort_values(by = 'encoded',
                       inplace = True)
    
    new_df.to_csv(filename,
                  sep = ';',
                  index = False,
                  encoding = 'utf-8')
    
    d = new_df['label'].value_counts().to_dict()
    
    return {int(k): int(v) for k, v in d.items()}

def GetUrl(driver, t):
    d = {'encoded': [],
         't00': [],
         't01': [],
         't10': [],
         't11': [],
         't20': [],
         't21': [],
         't30': [],
         't31': [],
         't40': [],
         't41': [],
         't50': [],
         't51': [],
         't6': [],
         'url': []}
    
    driver.find_element(By.XPATH, '//button[@class="btn btn-raised btn-primary"]').click()
    try:
        a_tags = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//tbody/tr/td/a')))
        for idx, a_tag in enumerate(a_tags):
            url = a_tag.get_attribute('href').strip()
            t[-1] = '{}'.format(idx)
            d['encoded'].append('|'.join(t))
            d['t00'].append(t[0])
            d['t01'].append(t[1])
            d['t10'].append(t[2])
            d['t11'].append(t[3])
            d['t20'].append(t[4])
            d['t21'].append(t[5])
            d['t30'].append(t[6])
            d['t31'].append(t[7])
            d['t40'].append(t[8])
            d['t41'].append(t[9])
            d['t50'].append(t[10])
            d['t51'].append(t[11])
            d['t6'].append(t[12])
            d['url'].append(url)
    except TimeoutException:
        d['encoded'].append('|'.join(t))
        d['t00'].append(t[0])
        d['t01'].append(t[1])
        d['t10'].append(t[2])
        d['t11'].append(t[3])
        d['t20'].append(t[4])
        d['t21'].append(t[5])
        d['t30'].append(t[6])
        d['t31'].append(t[7])
        d['t40'].append(t[8])
        d['t41'].append(t[9])
        d['t50'].append(t[10])
        d['t51'].append(t[11])
        d['t6'].append(t[12])
        d['url'].append(np.nan)
    
    return d

def GetUrlByLabelAndIndex(args):
    label, index, isheadless, reverse, uf = args

    df = pd.read_csv('urls/patterns.csv',
                     sep = ';',
                     dtype = str,
                     encoding = 'utf-8')
    
    df = df[df['label'] == str(label)]
    df.reset_index(drop = True, inplace = True)
    df = df.iloc[[index]]

    d = {'encoded': [],
         't00': [],
         't01': [],
         't10': [],
         't11': [],
         't20': [],
         't21': [],
         't30': [],
         't31': [],
         't40': [],
         't41': [],
         't50': [],
         't51': [],
         't6': [],
         'url': []}
    
    if isheadless:
        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')

        driver = webdriver.Firefox(options = options)
    else:
        driver = webdriver.Firefox()
    
    try:
        url = 'https://datasus.saude.gov.br/transferencia-de-arquivos/'
        driver.get(url)

        for _, row in df.iterrows():
            _, t00, t01, t10, t11, t20, t21, label = row
            
            select0_tag = driver.find_element(By.XPATH, '//select[@id="mySelect"]') # fonte
            _ = FindTags(driver, '//select[@id="mySelect"]/child::option')
            select0_tag_form = Select(select0_tag)
            select0_tag_form.select_by_value(t00)

            select1_tag = driver.find_element(By.XPATH, '//select[@id="modSelect"]') # modalidade
            _ = FindTags(driver, '//select[@id="modSelect"]/child::option')
            select1_tag_form = Select(select1_tag)
            select1_tag_form.select_by_value(t10)

            select2_tag = driver.find_element(By.XPATH, '//select[@id="tipo_arquivo"]') # tipo de dado
            _ = FindTags(driver, '//select[@id="tipo_arquivo"]/child::option')
            select2_tag_form = Select(select2_tag)
            select2_tag_form.select_by_value(t20)

            style3 = FindTagValue(driver, '//div[@id="linha_competencia"]', 'style') # ano
            style5 = FindTagValue(driver, '//div[@id="linha_uf"]', 'style') # uf

            if style3 == 'display: none;':
                if style5 == 'display: none;':
                    ### Label 1 ###
                    t = [t00, t01, t10, t11, t20, t21, '', '', '', '', '', '', '0']
                    new_d = GetUrl(driver, t)
                    # print('Label #1 -> {}'.format(new_d))

                    for key in new_d.keys():
                        d[key] = d[key] + new_d[key]
                    ### Label 1 ###
                else:
                    ### Label 2 ###
                    select5_tag = driver.find_element(By.XPATH, '//select[@id="moduf"]') # uf
                    option5_tags = FindTags(driver, '//select[@id="moduf"]/child::option')
                    
                    if reverse:
                        option5_tags = option5_tags[::-1]

                    for option5_tag in option5_tags:
                        t50 = option5_tag.get_attribute('value')
                        t51 = option5_tag.get_attribute('innerText')
                        
                        if uf is None:
                            select5_tag_form = Select(select5_tag)
                            select5_tag_form.select_by_value(t50)

                            t = [t00, t01, t10, t11, t20, t21, '', '', '', '', t50, t51, '0']
                            new_d = GetUrl(driver, t)
                            # print('Label #2 -> {}'.format(new_d))

                            for key in new_d.keys():
                                d[key] = d[key] + new_d[key]

                            select5_tag_form.deselect_by_value(t50)
                        else:
                            if t50 in uf:
                                select5_tag_form = Select(select5_tag)
                                select5_tag_form.select_by_value(t50)

                                t = [t00, t01, t10, t11, t20, t21, '', '', '', '', t50, t51, '0']
                                new_d = GetUrl(driver, t)
                                # print('Label #2 -> {}'.format(new_d))

                                for key in new_d.keys():
                                    d[key] = d[key] + new_d[key]

                                select5_tag_form.deselect_by_value(t50)
                    ### Label 2 ###
            else:
                select4_tag = driver.find_element(By.XPATH, '//div[@id="box_mes"]') # mês
                style4 = select4_tag.get_attribute('style')

                if style4 == 'display: none;':
                    if style5 == 'display: none;':
                        ### Label 3 ###
                        select3_tag = driver.find_element(By.XPATH, '//select[@id="modAno"]')
                        option3_tags = FindTags(driver, '//select[@id="modAno"]/child::option')
                        
                        if reverse:
                            option3_tags = option3_tags[::-1]
                        
                        for option3_tag in option3_tags:
                            t30 = option3_tag.get_attribute('value')
                            t31 = option3_tag.get_attribute('innerText')
                            select3_tag_form = Select(select3_tag)
                            select3_tag_form.select_by_value(t30)

                            t = [t00, t01, t10, t11, t20, t21, t30, t31, '', '', '', '', '0']
                            new_d = GetUrl(driver, t)
                            # print('Label #3 -> {}'.format(new_d))

                            for key in new_d.keys():
                                d[key] = d[key] + new_d[key]
                            
                            select3_tag_form.deselect_by_value(t30)
                        ### Label 3 ###
                    else:
                        ### Label 4 ###
                        select3_tag = driver.find_element(By.XPATH, '//select[@id="modAno"]')
                        option3_tags = FindTags(driver, '//select[@id="modAno"]/child::option')
                        
                        if reverse:
                            option3_tags = option3_tags[::-1]
                        
                        for option3_tag in option3_tags:
                            t30 = option3_tag.get_attribute('value')
                            t31 = option3_tag.get_attribute('innerText')
                            select3_tag_form = Select(select3_tag)
                            select3_tag_form.select_by_value(t30)

                            select5_tag = driver.find_element(By.XPATH, '//select[@id="moduf"]')
                            option5_tags = FindTags(driver, '//select[@id="moduf"]/child::option')
                            
                            if reverse:
                                option5_tags = option5_tags[::-1]
                            
                            for option5_tag in option5_tags:
                                t50 = option5_tag.get_attribute('value')
                                t51 = option5_tag.get_attribute('innerText')
                                
                                if uf is None:
                                    select5_tag_form = Select(select5_tag)
                                    select5_tag_form.select_by_value(t50)

                                    t = [t00, t01, t10, t11, t20, t21, t30, t31, '', '', t50, t51, '0']
                                    new_d = GetUrl(driver, t)
                                    # print('Label #4 -> {}'.format(new_d))

                                    for key in new_d.keys():
                                        d[key] = d[key] + new_d[key]
                                    
                                    select5_tag_form.deselect_by_value(t50)
                                else:
                                    if t50 in uf:
                                        select5_tag_form = Select(select5_tag)
                                        select5_tag_form.select_by_value(t50)

                                        t = [t00, t01, t10, t11, t20, t21, t30, t31, '', '', t50, t51, '0']
                                        new_d = GetUrl(driver, t)
                                        # print('Label #4 -> {}'.format(new_d))

                                        for key in new_d.keys():
                                            d[key] = d[key] + new_d[key]
                                        
                                        select5_tag_form.deselect_by_value(t50)
                            select3_tag_form.deselect_by_value(t30)
                        ### Label 4 ###
                else:
                    if style5 == 'display: none;':
                        ### Label 5 ###
                        select3_tag = driver.find_element(By.XPATH, '//select[@id="modAno"]')
                        option3_tags = FindTags(driver, '//select[@id="modAno"]/child::option')

                        if reverse:
                            option3_tags = option3_tags[::-1]
                        
                        for option3_tag in option3_tags:
                            t30 = option3_tag.get_attribute('value')
                            t31 = option3_tag.get_attribute('innerText')
                            select3_tag_form = Select(select3_tag)
                            select3_tag_form.select_by_value(t30)

                            select4_tag = driver.find_element(By.XPATH, '//select[@id="modmes"]')
                            option4_tags = FindTags(driver, '//select[@id="modmes"]/child::option')
                            
                            if reverse:
                                option4_tags = option4_tags[::-1]
                            
                            for option4_tag in option4_tags:
                                t40 = option4_tag.get_attribute('value')
                                t41 = option4_tag.get_attribute('innerText')
                                select4_tag_form = Select(select4_tag)
                                select4_tag_form.select_by_value(t40)

                                t = [t00, t01, t10, t11, t20, t21, t30, t31, t40, t41, '', '', '0']
                                new_d = GetUrl(driver, t)
                                # print('Label #5 -> {}'.format(new_d))

                                for key in new_d.keys():
                                    d[key] = d[key] + new_d[key]

                                select4_tag_form.deselect_by_value(t40)
                            select3_tag_form.deselect_by_value(t30)
                        ### Label 5 ###
                    else:
                        ### Label 6 ###
                        select3_tag = driver.find_element(By.XPATH, '//select[@id="modAno"]')
                        option3_tags = FindTags(driver, '//select[@id="modAno"]/child::option')
                        
                        if reverse:
                            option3_tags = option3_tags[::-1]
                        
                        for option3_tag in option3_tags:
                            t30 = option3_tag.get_attribute('value')
                            t31 = option3_tag.get_attribute('innerText')
                            select3_tag_form = Select(select3_tag)
                            select3_tag_form.select_by_value(t30)

                            select4_tag = driver.find_element(By.XPATH, '//select[@id="modmes"]')
                            option4_tags = FindTags(driver, '//select[@id="modmes"]/child::option')
                            
                            if reverse:
                                option4_tags = option4_tags[::-1]
                            
                            for option4_tag in option4_tags:
                                t40 = option4_tag.get_attribute('value')
                                t41 = option4_tag.get_attribute('innerText')
                                
                                select4_tag_form = Select(select4_tag)
                                select4_tag_form.select_by_value(t40)

                                select5_tag = driver.find_element(By.XPATH, '//select[@id="moduf"]')
                                option5_tags = FindTags(driver, '//select[@id="moduf"]/child::option')
                                
                                if reverse:
                                    option5_tags = option5_tags[::-1]
                                
                                for option5_tag in option5_tags:
                                    t50 = option5_tag.get_attribute('value')
                                    t51 = option5_tag.get_attribute('innerText')
                                    
                                    if uf is None:
                                        select5_tag_form = Select(select5_tag)
                                        select5_tag_form.select_by_value(t50)

                                        t = [t00, t01, t10, t11, t20, t21, t30, t31, t40, t41, t50, t51, '0']
                                        new_d = GetUrl(driver, t)
                                        # print('Label #6 -> {}'.format(new_d))

                                        for key in new_d.keys():
                                            d[key] = d[key] + new_d[key]
                                        
                                        select5_tag_form.deselect_by_value(t50)
                                    else:
                                        if t50 in uf:
                                            select5_tag_form = Select(select5_tag)
                                            select5_tag_form.select_by_value(t50)

                                            t = [t00, t01, t10, t11, t20, t21, t30, t31, t40, t41, t50, t51, '0']
                                            new_d = GetUrl(driver, t)
                                            # print('Label #6 -> {}'.format(new_d))

                                            for key in new_d.keys():
                                                d[key] = d[key] + new_d[key]
                                            
                                            select5_tag_form.deselect_by_value(t50)
                                select4_tag_form.deselect_by_value(t40)
                            select3_tag_form.deselect_by_value(t30)
                        ### Label 6 ###
            select2_tag_form.deselect_by_value(t20)
            select1_tag_form.deselect_by_value(t10)
            select0_tag_form.deselect_by_value(t00)
        driver.quit()
    except:
        driver.quit()
    
    new_df = pd.DataFrame(d)
    filename = 'urls/output_label{}_index{:02d}.csv'.format(label, index)
    if os.path.isfile(filename):
        old_df = pd.read_csv(filename,
                             sep = ';',
                             dtype = str,
                             encoding = 'utf-8')
        
        ### MERGE ###
        new_df = pd.merge(old_df,
                          new_df,
                          on = 'encoded',
                          how = 'outer',
                          suffixes = ('', '_y'))
        
        cols = ['t00',
                't01',
                't10',
                't11',
                't20',
                't21',
                't30',
                't31',
                't40',
                't41',
                't50',
                't51',
                't6',
                'url']
        
        for col in cols:
            col_y = '{}_y'.format(col)
            new_df[col] = new_df[col].fillna(new_df[col_y])
        
        cols = ['encoded'] + cols
        new_df = new_df[cols]
        ### MERGE ###
    
    new_df.sort_values(by = 'encoded',
                       inplace = True)
    
    new_df.to_csv(filename,
                  sep = ';',
                  index = False,
                  encoding = 'utf-8')

def GetFileByLabelAndIndex(args):
    label, index = args

    filename = 'urls/output_label{}_index{:02d}.csv'.format(label, index)
    if os.path.isfile(filename):
        df = pd.read_csv(filename,
                         sep = ';',
                         dtype = str,
                         encoding = 'utf-8')
        
        for _, row in df.iterrows():
            url = row['url']
            if isinstance(url, str):
                # name
                name = url.split('/')[-1]
                name = re.sub(' ', '\ ', name)
                # name
                
                # path
                fields = row['encoded'].split('|')[::2]
                
                filtered_fields = []
                for field in fields:
                    if field != '':
                        filtered_fields.append(field)
                
                os.makedirs('datasets/', exist_ok = True)
                path = 'datasets/' + '/'.join(filtered_fields)
                path = re.sub(' ', '\ ', path)
                
                command_line = 'mkdir -p {}'.format(path)
                try:
                    os.system(command_line)
                except OSError as error:
                    print('Error0 (GetFileByLabelAndIndex): {}'.format(error))
                # path
                
                # download
                filename = '{}/{}'.format(path, name)

                status = os.path.isfile(filename)
                if status == False:
                    command_line = 'curl -s --compressed -o {} {}'.format(filename, url)
                    print(filename, url, command_line)

                    try:
                        os.system(command_line)
                    except OSError as error:
                        print('Error1 (GetFileByLabelAndIndex): {}'.format(error))
                # download

def DbcToCsv():
    os.system('cd crawler/blast-dbf; make clean; make') # compile the blast-dbf code

    paths = glob.glob('datasets/**/*.dbc',
                      recursive = True)
    n = len(paths)

    errors = []
    for i, path in enumerate(paths):
        name = path[:-4]
        print('DbcToCsv: {} {} {} {}'.format(n, i, len(errors), name))
        
        if os.path.isfile('{}.csv.xz'.format(name)) == False:
            try:
                os.system('./crawler/blast-dbf/blast-dbf {}.dbc {}.dbf'.format(name, name))
                dbf = simpledbf.Dbf5('{}.dbf'.format(name), codec = 'ISO-8859-1')
                df = dbf.to_dataframe()

                df.to_csv('{}.csv.xz'.format(name),
                          sep = ';',
                          index = False,
                          encoding = 'utf-8',
                          compression = 'xz')
                
                os.system('rm {}.dbf'.format(name))
            except:
                errors.append(name)
                s = pd.Series(errors,
                              name = 'paths')
                
                s.to_csv('errors.csv',
                         index = False,
                         encoding = 'utf-8')

def RmCsvXz():
    paths = glob.glob('datasets/**/*.csv.xz',
                      recursive = True)
    
    n = len(paths)
    for i, path in enumerate(paths):
        print('RmCsvXz: {} {} {}'.format(n, i, path))
        os.system('rm {}'.format(path))