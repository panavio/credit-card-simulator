def initialize():
    global cur_balance_owing_intst
    global cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_country, last_country2
    global status_disabled
    cur_balance_owing_intst = 0
    cur_balance_owing_recent = 0
    

    status_disabled=False
    #set last day and month as 1,1
    last_update_day, last_update_month = 1, 1
    
    last_country = None
    last_country2 = None
    
    MONTHLY_INTEREST_RATE = 0.05




def Check_valid_date(day, month):
    month_num_days=[31,29,31,30,31,30,31,31,30,31,30,31]
    #print("Check valid date for", day, ",",month)
    if ((isinstance(day, int)==True) and (isinstance(month, int)==True)):
        if (month!=-15910 and day!=-15910):
            if (month>12 or month<=0):
                #print("False(month not valid, should be in range of 1-12)")
                return False
            elif ((month_num_days[month-1]>=day) and (0<day)):
                return True
            else:
                #date not valid, should be in range of 1-", month_num_days[month-1]
                return False
        else:
            return True
    else:
        #print("False(input not valid, numbers should be integer)")
        return False





def date_same_or_later(day1, month1, day2, month2):
    if((Check_valid_date(day1,month1)==True) and (Check_valid_date(day2,month2)==True)):
        if ((month1==month2) and (day1 >= day2)):
            return True
        elif (month1>month2):
            return True
        else:
            print(day1, ",",month1, "is not the same date or occurs later than ", day2,",",month2)
            return False
    else:
        return False
        



def all_three_different(c1, c2, c3):
    if( (c1==None) or (c1==None) or (c3==None)):
        return False
    if ((c1!=c2) and (c2!=c3) and (c1!=c3)):
        return True
    else:
        return False



        
def purchase(amount, day, month, country):
    global cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_country, last_country2
    global status_disabled
    if (status_disabled==False):
        if(all_three_different(country, last_country, last_country2)==False):
            if (date_same_or_later(day,month,last_update_day, last_update_month)==True):
                amount_owed(day,month)
                last_update_day, last_update_month=day,month
                cur_balance_owing_recent=cur_balance_owing_recent+amount
                last_country2=last_country
                last_country = country
            else:
                return "error"


        else:
            status_disabled=True
            #print("error")
            return "error"  
    else:
        return "error"
    



def amount_owed(day, month):
    global last_update_day,last_update_month,cur_balance_owing_recent,cur_balance_owing_intst
    if (date_same_or_later(day,month,last_update_day,last_update_month)==True):
        if month!=last_update_month:
            cur_balance_owing_intst=cur_balance_owing_intst*(1.05**(month-last_update_month))+cur_balance_owing_recent*(1.05**(month-last_update_month-1))
            cur_balance_owing_recent=0
        last_update_day, last_update_month=day,month
        return cur_balance_owing_intst+cur_balance_owing_recent
        
    else:
        return "error"

    



def pay_bill(amount, day, month):
    global last_update_day,last_update_month,cur_balance_owing_recent,cur_balance_owing_intst
    if (date_same_or_later(day,month,last_update_day,last_update_month)==True):
        if ((cur_balance_owing_recent+cur_balance_owing_intst)>=amount):
            amount_owed(day,month)
            if cur_balance_owing_intst>=amount:
                cur_balance_owing_intst=cur_balance_owing_intst-amount
            elif cur_balance_owing_intst>=0 :
                cur_balance_owing_recent=cur_balance_owing_recent-(amount-cur_balance_owing_intst)
                cur_balance_owing_intst=0
            else:
                return "unknown error in pay bill (cur balance owing interese is negative)"
        else:
            return "error, amount paid is too much"
    else:
        return "error"
        



# Initialize all global variables outside the main block.
initialize()		

if __name__ == '__main__':
    # Describe your testing strategy and implement it below.
    # What you see here is just the simulation from the handout, which
    # doesn't work yet.

    initialize()
    purchase(80, 8, 1, "Canada")
    
    print("Now owing:", amount_owed(8, 1))      # 80.0                              (Test1)
    pay_bill(50, 2, 2)
    print("Now owing:", amount_owed(2, 2))      # 30.0     (=80-50)                 (Test2)
    print("Now owing:", amount_owed(6, 3))      # 31.5     (=30*1.05)               (Test3)
    purchase(40, 6, 3, "Canada")
    print("Now owing:", amount_owed(6, 3))      # 71.5     (=31.5+40)               (Test4)
    pay_bill(30, 7, 3)

    print("Now owing:", amount_owed(7, 3))      # 41.5     (=71.5-30)               (Test5)
    print("Now owing:", amount_owed(1, 5))      # 43.65375 (=1.5*1.05*1.05+40*1.05) (Test6)
    purchase(40, 2, 5, "France")
    print("Now owing:", amount_owed(2, 5))      # 83.65375                          (Test7)
    print(purchase(50, 3, 5, "United States"))  # error    (3 diff. countries in    (Test8)
                                                #          a row)
                                                
    print("Now owing:", amount_owed(3, 5))      # 83.65375 (no change, purchase     (Test9)
                                                #           declined)
    print(purchase(150, 3, 5, "Canada"))        # error    (card disabled)          (Test10)
    print("Now owing:", amount_owed(1, 6))      # 85.8364375                        (Test11)
                                                # (43.65375*1.05+40)