import pandas as pd
import tabula
import re

dfs=tabula.read_pdf("9_2023_Unredeemed_Tax_Sale.pdf",pages="all")
dfs = pd.concat(dfs)
dfs=dfs.fillna('')

pattern = r'\d{2}-\d{2}-\d{3}-\d{3}' 
filtered_df = dfs[dfs['Unnamed: 0'].str.contains(pattern, regex=True)]
filtered_df['Total Due For'] = filtered_df['Total Due For'].str.replace('$', '').str.replace(',', '').astype(float)
filtered_df = filtered_df[filtered_df['Total Due For'] > 0]


def filter_pattern(column,pattern):
    matches=[]
    pattern=pattern
    for index, row in filtered_df.iterrows():
        text = row[column]
        variable_matches = re.findall(pattern, text)
        matches.extend(variable_matches)
    return matches

def filter(column):
    filter_data=filtered_df[column].tolist()
    clean_value= [s.replace('$', '').replace(',','') for s in filter_data]
    return clean_value
    

def apn_stripped():
    pattern = r'\d{2}-\d{2}-\d{3}-\d{3}'
    clean_value_apn_stripped=[]
    matches=filter_pattern('Unnamed: 0',pattern)
    for i in matches:
        i=i.replace('-','')
        clean_value_apn_stripped.append(i)

    clean_value_apn_stripped = [s.replace('-', '') for s in matches]
    return clean_value_apn_stripped


def year_and_certificate_number():
    pattern = r'\d{9}' 
    matches=[]
    clean_value_year=[]
    matches=filter_pattern('Unnamed: 0',pattern)
    for i in matches:
        clean_value_year.append(int(i[0:4]))
    clean_value_certificate_number=[int(i) for i in matches]
    return clean_value_year,clean_value_certificate_number

def sold():
    pattern = r'(\d{1,2}/\d{1,2}/\d{4})'
    clean_value_date_sold=[]
    clean_value_date_sold=filter_pattern('Unnamed: 0',pattern)
    return  clean_value_date_sold

def tsi_tax_amount():
    tsi_tax_amount=filtered_df['Unnamed: 2'].tolist()
    tsi_tax_amount2=filtered_df['Unnamed: 1'].tolist()
    clean_value_tsi_penalty_before={}
    clean_value_tsi_tax_amount = [s.replace('$', '').replace(',','') for s in tsi_tax_amount]
    clean_value_tsi_tax_amount2 = [s.replace('$', '').replace(',','') for s in tsi_tax_amount2]

    def convert_to_float(count,value):
        parts = value.split()
        if len(parts)>1:
            clean_value_tsi_tax_amount[count-1]=parts[0]
            clean_value_tsi_penalty_before[count]=parts[1]
        return sum(map(float, parts)) 
    count=0
    for value in clean_value_tsi_tax_amount:
        count=count+1
        convert_to_float(count,value)

    tsi_penalty=filtered_df['Penalty'].tolist()
    clean_value_tsi_tax_amount_before={}

    clean_value_tsi_penalty = [s.replace('$', '').replace(',','') for s in tsi_penalty]
    def convert_to_float(count,value):
        parts = value.split()
        if len(parts)>1:
            clean_value_tsi_penalty[count-1]=parts[0]
            clean_value_tsi_tax_amount_before[count]=parts[1]
        return sum(map(float, parts)) 

    for value in clean_value_tsi_penalty:
        convert_to_float(count,value)

    for key,value in clean_value_tsi_tax_amount_before.items():
        clean_value_tsi_tax_amount[key-1]=value


    for key,value in clean_value_tsi_penalty_before.items():
        clean_value_tsi_penalty[key-1]=value

    for i in range(len(clean_value_tsi_tax_amount)):
        if clean_value_tsi_tax_amount[i] == '':

        
            clean_value_tsi_tax_amount[i]=clean_value_tsi_tax_amount2[i]
            
    tsi_tax_amounts=filtered_df["Unnamed: 0"].tolist()
    unnamed_tax_amount=[]


    for i in tsi_tax_amounts:
        total_data=i.split(" ")

        if len(total_data)==4:

            unnamed_tax_amount.append(total_data[3])
        else:
            unnamed_tax_amount.append("")
    unnamed_tax_amount = [string.replace('$', '') for string in unnamed_tax_amount]
    for i in range(len(clean_value_tsi_tax_amount)):
        if clean_value_tsi_tax_amount[i] == '':

    
            clean_value_tsi_tax_amount[i]=unnamed_tax_amount[i]

    
    return clean_value_tsi_tax_amount,clean_value_tsi_penalty



def tsi_penalty():
    tsi_penalty=filtered_df['Penalty'].tolist()
    clean_value_tsi_penalty = [s.replace('$', '').replace(',','') for s in tsi_penalty]
    clean_value_tsi_penalty = [float(value) if value.strip() != "" else 0.0 for value in clean_value_tsi_penalty]
    return clean_value_tsi_penalty

def tsi_cost_fee(clean_value_tsi_penalty):
    
    clean_value_tsi_cost=[]
    clean_value_tsi_fee=[]

    for page_number in range(1, 90):  
    
        page_data = tabula.read_pdf('9_2023_Unredeemed_Tax_Sale.pdf', pages=page_number, multiple_tables=True)
        dfss = pd.concat(page_data)
        dfss=dfss.fillna('')
        pattern = r'\d{2}-\d{2}-\d{3}-\d{3}'  
        filtered_dfs = dfss[dfss['Unnamed: 0'].str.contains(pattern, regex=True)]
    
        try:

            tsi_costs=filtered_dfs['Unnamed: 3'].tolist()
        
            for i in tsi_costs:
                i=i.replace('$','').replace(',','')
                cost,fee=i.split()
                clean_value_tsi_cost.append(cost)
                clean_value_tsi_fee.append(fee)
    
        except:
            tsi_cost=filtered_dfs['Unnamed: 3'].tolist()
            for i in tsi_cost:
                i=i.replace('$','').replace(',','')
                clean_value_tsi_cost.append(i)
        
            tsi_fee=filtered_dfs['Unnamed: 4'].tolist()
            for i in tsi_fee:
                i=i.replace('$','').replace(',','')
                clean_value_tsi_fee.append(i)
        for i in range(len(clean_value_tsi_cost)):
            if clean_value_tsi_cost[i] == '':
                data=clean_value_tsi_penalty[i].split(" ")[1]
                data2=clean_value_tsi_penalty[i].split(" ")[0]
                clean_value_tsi_cost[i]=data
                clean_value_tsi_penalty[i]=data2
    return clean_value_tsi_cost,clean_value_tsi_fee

def total_sold():
  
    tsi_back_tax=filtered_df['Back Tax Total Sold'].tolist()
    clean_value_tsi_back_tax=[]
    clean_value_total_sold=[]
    clean_value_tsi_back= [s.replace('$', '').replace(',','') for s in tsi_back_tax]

    def process_string(s):

        parts = s.split()
        
        return [float(parts[0]), float(parts[1]), parts[2]]

    result = [process_string(item) for item in clean_value_tsi_back]
    for i in result:
        clean_value_tsi_back_tax.append(i[0])
        clean_value_total_sold.append(i[1])
        


    return clean_value_total_sold

def tsi_back_tax():
    tsi_back_tax=filtered_df['Back Tax'].tolist()
    clean_value_tsi_back_tax= [s.replace('$', '').replace(',','') for s in tsi_back_tax]
    return clean_value_tsi_back_tax


def extension_date():
 
    clean_value_extension_date=[]


    for page_number in range(1, 90):  # Assuming a 40-page document
        
        page_data = tabula.read_pdf("9_2023_Unredeemed_Tax_Sale.pdf", pages=page_number, area=(100,100, 800, 900))
        dfss = pd.concat(page_data)
        dfss=dfss.fillna('')

        pattern = r'(\d{1,2}/\d{1,2}/\d{4})'
            

        
        for index, row in dfss.iterrows():
            text = row['Back Tax Total Sold']
            # Use re.findall() to find all matches in the text
            variable_matches = re.findall(pattern, text)
            # Extend the 'matches' list with the matches from this row
            
            # if len(variable_matches)==1:
            #     for i in variable_matches:
            #         clean_value_extension_dates.append(i)
        
            clean_value_extension_date.extend(variable_matches)


    clean_value_extension_date=clean_value_extension_date[0:661]
    return clean_value_extension_date

def total_due():
    clean_value_total_due = filtered_df['Total Due For']
    return clean_value_total_due

def ssi_tax_amount():
    clean_value_ssi_tax_amount = filter('Unnamed: 7')
    return clean_value_ssi_tax_amount

def ssi_penalty():
    clean_value_ssi_penalty = filter('Penalty.1')
    return clean_value_ssi_penalty

def ssi_cost():
    clean_value_ssi_cost = filter('Unnamed: 8')
    return clean_value_ssi_cost

def back_tax():
    clean_value_ssi_back_tax=filter('Back Tax')
    return clean_value_ssi_back_tax

def ssi_total_sold():
    clean_value_ssi_total_sold= filter('Unnamed: 9')
    return clean_value_ssi_total_sold

clean_value_apn_stripped=apn_stripped()


clean_value_year,clean_value_certificate_number=year_and_certificate_number()


clean_value_date_sold=sold()

clean_value_tsi_tax_amount,clean_value_tsi_penalty=tsi_tax_amount()

# clean_value_tsi_penalty=tsi_penalty()

clean_value_tsi_cost,clean_value_tsi_fee=tsi_cost_fee(clean_value_tsi_penalty)


clean_value_total_sold=total_sold()

clean_value_extension_date=extension_date()

clean_value_ssi_tax_amount=ssi_tax_amount()

clean_value_ssi_penalty=ssi_penalty()

clean_value_ssi_cost=ssi_cost()

clean_value_ssi_back_tax=back_tax()

clean_value_ssi_total_sold=ssi_total_sold()

clean_value_total_due=total_due()





final_data= pd.DataFrame({'apn_stripped': clean_value_apn_stripped, 'year': clean_value_year,'sold_date': clean_value_date_sold,'certificate_number': clean_value_certificate_number,'tsi_tax_amount': clean_value_tsi_tax_amount,'tsi_tax_penalty': clean_value_tsi_penalty
,'tsi_costs':clean_value_tsi_cost,'tsi_fee':clean_value_tsi_fee,'tsi_total_sold': clean_value_total_sold,'extension_date':clean_value_extension_date,'ssi_tax_amount':clean_value_ssi_tax_amount,'ssi_penalty':clean_value_ssi_penalty,'ssi_costs':clean_value_ssi_cost,'ssi_back_tax_drainage':clean_value_ssi_back_tax,
'ssi_total':clean_value_ssi_total_sold,'total_due':clean_value_total_due})


final_data['fips']=[11723]*len(final_data)
file_path = 'final_data.csv'
final_data.to_csv(file_path, index=False)
