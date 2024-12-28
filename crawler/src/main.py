import sys
from ebay.getCode import ebay_run
from amazon.getCode import amazon_run

if __name__ == "__main__":
    keyword = ""
    if len(sys.argv) > 2:
        web_num = sys.argv[1]
        # print(web_num)
        # print(sys.argv)
        # sys.exit(1)
        for i in range(2, len(sys.argv)):
            keyword = keyword + " " + sys.argv[i]
        if (web_num == '0'): 
            amazon_run(keyword)
        elif (web_num == '1'): 
            ebay_run(keyword)
        else:
            print("Web number should be 0 or 1.")
            
    else:
        print("The format should be: python3 main.py <web_num> <keyword keyword keyword>. Web number should be 0 (Amazon) or 1 (ebay).")
        sys.exit(1)
