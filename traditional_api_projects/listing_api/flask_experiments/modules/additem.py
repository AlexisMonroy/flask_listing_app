import os
import sqlite3
import requests
import datetime 
from modules.schedule import schedule_listings



def add_item(product_list, token, call_header, url):
    pic_site = "https://alexismonroy.github.io/images/"

    data_folder = 'C:/Users/alexi/dev/ebay_api/ebay_api/traditional_api_projects/listing_api/flask_experiments/data'

    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Get the path to the resp_output directory
    resp_output_dir = os.path.join(current_dir, '..', 'resp_output')

    # Create the resp_output directory if it doesn't exist
    if not os.path.exists(resp_output_dir):
        os.makedirs(resp_output_dir)

    # Get the path to the file to write to
    file_path = os.path.join(resp_output_dir, 'api_call_response.txt')
    file_path_verify_data = os.path.join(resp_output_dir, 'additem_data.txt')
    file_path_start_end = os.path.join(resp_output_dir, 'start_end.txt')
    
    conn = sqlite3.connect(os.path.join(data_folder, 'inventory.db'))

    cursor = conn.cursor()

    query = '''SELECT PRODUCT_ID FROM posted WHERE PRODUCT_ID = ?'''
    select_item = '''SELECT * FROM books WHERE ID = ?'''


    #check if the product id is in the posted table; has it been listed?
    call_list = []
    pic_call_list = []
    add_item_list = []
    schedule_times = schedule_listings(len(product_list))
    for i in range(0, len(product_list)):
        product_id_tuple = product_list[i]
        product_id = int(product_id_tuple[0])
        cursor.execute(query, product_list[i])
        posted_result = cursor.fetchone()
        #print(posted_result)
        if posted_result is None:
            print("No match found")
            #if the product id is not in the posted table, then retrieve the item details from the books table
            cursor.execute(select_item, product_list[i])
            item_details = cursor.fetchone()
            #initialize the count variable
            time_index = i
            count = 0
            with open('add_item_output.text', 'a') as f:
                print("Start: ", datetime.datetime.now(), file=f)
                print("ITEM DETAILS:", item_details, file=f)
                print("TYPE: ", type(item_details), file=f)
                print("End: ", datetime.datetime.now(), file=f)
            #create a dictionary to store the item details
            item_dict = {'item_id': None, 'Title': None, 'Author': None, 'Units': None, 'Illustrator': None, 'Genre': None, 'Publisher': None, 'Publication Year': None, 'Price': None, 'Description': None, 'Condition': None, 'Condition Description': None, 'Book Format': None, 'Features': None, 'Language': None, 'Topic': None, 'Book Series': None, 'Book Type': None, 'Narrative Type': None, 'Edition': None, 'Manufactured': None, 'Inscibed': None, 'Intended Audience': None, 'Vintage': None, 'Signed': None, 'Pictures': None, 'Height': None, 'Width': None, 'Length': None, 'Weight': None, 'Weight_Minor': None}
            name_value_list = []
            #iterate through the dictionary and assign the item details to the dictionary keys
            for key in item_dict:
                item_dict[key] = item_details[count]
                #add name value pairs to a list
                if key in ['Title', 'Author', 'Illustrator', 'Genre', 'Publisher', 'Publication Year', 'Book Format', 'Features', 'Language', 'Topic', 'Book Series', 'Book Type', 'Narrative Type', 'Edition', 'Manufactured', 'Inscibed', 'Intended Audience', 'Vintage', 'Signed']:
                    name_value_list.append((key, item_dict[key]))
                #increment the count variable
                count += 1
            #write the item details to a text file
            with open('add_item_output.text', 'a') as f:
                print("\nStart: ", datetime.datetime.now(), file=f)
                print("Item Details:\n", item_details, file=f)
                print("Item Dict:\n", item_dict, file=f)
                print("Name Value List:\n", name_value_list, file=f)
                print("End: ", datetime.datetime.now(), file=f)
            #print("\nName Value List:\n",name_value_list)
            name_value_call = ""
            for i in range(0, len(name_value_list)):
                k = 0
                j = 1
                if name_value_list[i][j] != "":
                    #store the value in a string
                    name_value_string = str(name_value_list[i][j])
                    #count the number of words in the value
                    num_words = len(name_value_string.split(','))
                    if num_words > 1:
                        #split the value into a list of words
                        words = name_value_string.split(',')
                        for word in words:
                            #add each word to the name value call
                            #store the names and values in variables
                            name = name_value_list[i][k]
                            value = word.strip()
                            name_value = f'''<NameValueList><Name>{name}</Name><Value>{value}</Value></NameValueList>'''
                            name_value_call = name_value_call + name_value
                    else:
                        #add the name value pair to the name value call
                        #store the names and values in variables
                        name = name_value_list[i][k]
                        value = name_value_list[i][j]
                        name_value = f'''<NameValueList><Name>{name}</Name><Value>{value}</Value></NameValueList>'''
                        name_value_call = name_value_call + name_value
            if name_value_call != "":
                call_list.append(name_value_call)
            with open('add_item_output.text', 'a') as f:
                print("\nStart: ", datetime.datetime.now(), file=f)
                print("Time:\n", datetime.datetime.now(), file=f)
                print("Call List: ", call_list, file=f)
                print("End: ", datetime.datetime.now(), file=f)
                #print the time the call was made
                

            #get the number of pictures
            num_pics = item_dict['Pictures']
            pic_details = ""
            #append the picture name
            for i in range(0, num_pics):
                #store the picture name in a variable and delete the spaces:
                og_picture = item_dict['Title']
                picture = og_picture.replace(" ", "")
                picture_name = picture + "/"+ picture + str(i)
                #print("\nPicture Name:\n", picture_name)
                pic_location = pic_site + picture_name + ".jpg"
                pic_details = pic_details + f'''<PictureURL>{pic_location}</PictureURL>'''
                #print("\nPicture Call:\n", pic_details)
            #pic_call = f'''<PictureDetails>{pic_details}</PictureDetails>'''
            
            if pic_details != "":
                pic_call_list.append(pic_details)
            with open('add_item_output.text', 'a') as f:
                print("\nStart:\n", datetime.datetime.now(), file=f)
                print("\nPicture Call List: ", pic_call_list, file=f)
                print("\nEnd:\n", datetime.datetime.now(), file=f)
                

            additem_data = f'''<?xml version="1.0" encoding="utf-8"?>
  <AddItemRequest xmlns="urn:ebay:apis:eBLBaseComponents">
    <RequesterCredentials>
      <eBayAuthToken>{token}</eBayAuthToken>
    </RequesterCredentials>
    <ErrorLanguage>en_US</ErrorLanguage>
    <WarningLevel>High</WarningLevel>
    <Item>
      <Title>{item_dict['Title']}</Title>
      <Description>
        {item_dict['Description']}
      </Description>
      <PrimaryCategory>
        <CategoryID>261186</CategoryID>
      </PrimaryCategory>
      <StartPrice>{item_dict['Price']}</StartPrice>
      <CategoryMappingAllowed>true</CategoryMappingAllowed>
      <ConditionID>5000</ConditionID>
      <ConditionDescription>{item_dict['Condition']}</ConditionDescription>
      <Country>US</Country>
      <Currency>USD</Currency>
      <DispatchTimeMax>1</DispatchTimeMax>
      <ListingDuration>GTC</ListingDuration>
      <ListingType>FixedPriceItem</ListingType>
      <PictureDetails>
        {pic_details}
      </PictureDetails>
      <PostalCode>90260</PostalCode>
      <Quantity>1</Quantity>
      <ItemSpecifics>     
      {name_value_call}
      </ItemSpecifics>
      <ScheduleTime>{schedule_times[time_index]}</ScheduleTime>  
      <ReturnPolicy>
        <ReturnsAcceptedOption>ReturnsAccepted</ReturnsAcceptedOption>
        <RefundOption>MoneyBack</RefundOption>
        <ReturnsWithinOption>Days_30</ReturnsWithinOption>
        <ShippingCostPaidByOption>Buyer</ShippingCostPaidByOption>
      </ReturnPolicy>
      <ShippingDetails>
        <ShippingType>Calculated</ShippingType>
        <ShippingServiceOptions>
          <ShippingService>USPSMedia</ShippingService>
          <ShippingServicePriority>1</ShippingServicePriority>         
        </ShippingServiceOptions>
        <ShippingServiceOptions>
            <ShippingService>USPSPriority</ShippingService>
            <ShippingServicePriority>2</ShippingServicePriority>
        </ShippingServiceOptions>
      </ShippingDetails>
      <ShippingPackageDetails>
        <MeasurementUnit>English</MeasurementUnit>
        <PackageDepth unit="inches" measurementSystem="English">{item_dict['Height']}</PackageDepth>
        <PackageLength unit="inches" measurementSystem="English">{item_dict['Length']}</PackageLength>
        <PackageWidth unit="inches" measurementSystem="English">{item_dict['Width']}</PackageWidth>
        <ShippingPackage>PackageThickEnvelope</ShippingPackage>
        <WeightMajor unit="lbs" measurementSystem="English">{item_dict['Weight']}</WeightMajor>
        <WeightMinor unit="oz" measurementSystem="English">{item_dict['Weight_Minor']}</WeightMinor>
      </ShippingPackageDetails>
      <Site>US</Site>
    </Item>
  </AddItemRequest>'''
            
            add_item_list.append(additem_data)
            #print("\nCALL:\n", verify_data)             
            #print(token)
            
            cursor.execute("SELECT PRODUCT_ID, MARKET_ID FROM pending where PRODUCT_ID = ?", (product_id,))
            pending = cursor.fetchall()
            cursor.execute("INSERT OR IGNORE INTO posted(PRODUCT_ID, MARKET_ID, DATE_TIME) VALUES (?, ?, datetime('now', 'localtime'))", (pending[0][0], pending[0][1],))
            conn.commit()
            cursor.execute("DELETE FROM pending WHERE PRODUCT_ID = ?", (product_id,))
            conn.commit()
            print("Product ID: ", product_id)
            with open('add_item_output.text', 'a') as f:
                print("\nTime: ", datetime.datetime.now(), file=f)
                print("\nVerify Data: ", additem_data, file=f)
                print("\nScheduled for: ", schedule_times[time_index], file=f)
                print("\nPOSTED", file=f)
            print("\nPOSTED")
        else:
            print("Item has already been posted")
    #print the end time to call_output.txt
    with open(file_path_verify_data, 'a') as f:
        f.write(str(add_item_list))
        print("TYPE:\n", type(add_item_list))
        with open(file_path_start_end, 'w') as f:
            f.write("START:\n:" + str(datetime.datetime.now()))
    
    additem_item_call = 'AddItem'
    use_additem_item = True
    if use_additem_item:
        call_name = additem_item_call
        call_header['X-EBAY-API-CALL-NAME'] = call_name
        header = call_header
    
    additem_responses = []
    for i in range(0, len(add_item_list)):
        try:
            if add_item_list[i] is not None:
                additem_response = requests.post(url, headers=header, data=add_item_list[i])
                print(additem_response.status_code)
                #print(additem_response.text)
                print("Done with API Call")
                with open(file_path, 'a') as f:
                    f.write("Start:\n:" + str(datetime.datetime.now()))
                    f.write("\n") 
                    f.write(str(len(additem_data)))
                    f.write("\n")
                    f.write(str(additem_response))
                    f.write("\n")
                    f.write(str(additem_response.text))
                    f.write("\n")
                    f.write("Scheduled for: " + str(schedule_times[time_index]))
                    f.write("\n")
                    f.write("End:\n:" + str(datetime.datetime.now()))
                    f.write("\n")
                additem_responses.append(additem_response.text)
            else:
                additem_responses.append("Nothing to post")
    
        except Exception as e:
            print(e)
            print("Error with API Call")
            with open('error.text', 'a') as f:
                f.write("\n")
                f.write("Start:\n:" + str(datetime.datetime.now()))
                f.write(str(len(additem_data)))
                f.write(str(e))
                f.write("\n")
                f.write(item_dict['Title'])
                print(item_dict['Title'])
                print("End:\n:" + str(datetime.datetime.now()))
            additem_responses.append(e)
    
    with open('add_item_output.text', 'a') as f:
        print("\nEnd of Program:\n", datetime.datetime.now(), file=f)
    with open(file_path_start_end, 'a') as f:
        f.write("END:\n:" + str(datetime.datetime.now()))
        
    conn.close()
    print("\nConnection Closed\n")
    return additem_responses

    
