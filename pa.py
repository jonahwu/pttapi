from PyPtt import PTT
import sys
import time

ptt_bot = PTT.API(
    # (預設值) Chinese
    # language=PTT.i18n.language.CHINESE,
    language=PTT.i18n.language.ENGLISH)
ptt_id='wcmein'
password='wcmwcm'
Board='Stock'
BoardLastID=0

try:
    ptt_bot.login(ptt_id, password)
except PTT.exceptions.LoginError:
    ptt_bot.log('登入失敗')
    sys.exit()
except PTT.exceptions.WrongIDorPassword:
    ptt_bot.log('帳號密碼錯誤')
    sys.exit()
except PTT.exceptions.LoginTooOften:
    ptt_bot.log('請稍等一下再登入')
    sys.exit()
ptt_bot.log('登入成功')

def crawl_handler1(post_info):
    if post_info.delete_status != PTT.data_type.post_delete_status.NOT_DELETED:
        if post_info.delete_status == PTT.data_type.post_delete_status.MODERATOR:
            print(f'[板主刪除][{post_info.author}]')
        elif post_info.delete_status == PTT.data_type.post_delete_status.AUTHOR:
            print(f'[作者刪除][{post_info.author}]')
        elif post_info.delete_status == PTT.data_type.post_delete_status.UNKNOWN:
            print(f'[不明刪除]')
        return

    print(f'[{post_info.aid}][{post_info.title}]')

def crawl_handler(post_info):
    print(post_info.index, post_info.list_date, post_info.title)
    return

def parseRangeDataByID():
    test_range =20
    test_board=Board
    newest_index = ptt_bot.get_newest_index(
        PTT.data_type.index_type.BBS,
        board=test_board)
    print('the newest index:',newest_index)
    start_index = newest_index - test_range + 1

    error_post_list, del_post_list = ptt_bot.crawl_board(
    PTT.data_type.crawl_type.BBS,
    crawl_handler,
    test_board,
    # 使用 index 來標示文章範圍
    start_index=start_index,
    end_index=newest_index,
    #search_type=search_type,
    #search_condition=condition,
    # 使用 aid 來標示文章範圍
    # Since 0.8.27
    # start_aid=start_aid,
    # end_aid=end_aid,
    # index 與 aid 標示方式擇一即可
    # will not resolve content and date...
    query=True
    )
    print('------ show list result ----')
    print(error_post_list)
    """
    if len(error_post_list) > 0:
        print('格式錯誤文章: \n' + '\n'.join(str(x) for x in error_post_list))
    else:
        print('沒有偵測到格式錯誤文章')

    if len(del_post_list) > 0:
        print(f'共有 {len(del_post_list)} 篇文章被刪除')
    """


def getBoardLastID():
    global BoardLastID
    test_list = [
    #('Python', PTT.data_type.post_search_type.KEYWORD, '[公告]')
    (Board)
    ]
    last_index=0
    # here we got no searching
    for (test_board) in test_list:
        last_index = ptt_bot.get_newest_index(
            PTT.data_type.index_type.BBS,
            board=test_board)

    BoardLastID=last_index

    return last_index


def getDataBySearch():
    test_list = [
    #('Python', PTT.data_type.post_search_type.KEYWORD, '[公告]')
    (Board, PTT.data_type.post_search_type.KEYWORD, '聯亞')
    ]

    for (test_board, search_type, condition) in test_list:
        last_index = ptt_bot.get_newest_index(
            PTT.data_type.index_type.BBS,
            board=test_board)
        index = ptt_bot.get_newest_index(
            PTT.data_type.index_type.BBS,
            test_board,
            search_type=search_type,
            search_condition=condition,
        )
        print(f'{test_board} 最新文章編號 {last_index}')
        print(f'{test_board} Keyword最新文章編號 {index}')

        post = ptt_bot.get_post(
            test_board,
            post_index=index,
            search_type=search_type,
            search_condition=condition,
        )

        print('標題:')
        print(post.title)
        #print('內文:')
        #print(post.content)
        #print('=' * 50)

        print('TIME:')
        print(post.date)
        print(post.list_date)
        print('--------------------------------')
        time.sleep(3)

def XgetDataByID():
    for i in range(0,20):
        idx=7486+i
        post_info = ptt_bot.get_post(
            'Python',
            post_index=idx)
            #post_index=7486)

        print('Board: ' + post_info.board)
        print('AID: ' + post_info.aid)
        print('index:' + str(post_info.index))
        print('Author: ' + post_info.author)
        print('Date: ' + post_info.date)
        print('Title: ' + post_info.title)
        print('content: ' + post_info.content)
        print('Money: ' + str(post_info.money))
        print('URL: ' + post_info.web_url)
        print('IP: ' + post_info.ip)
        # 在文章列表上的日期
        print('List Date: ' + post_info.list_date)
        print('地區: ' + post_info.location)
        # Since 0.8.19
        # 有可能為 None，因為不是每篇文在文章列表都有推文數
        try:
            print('文章推文數: ' + post_info.push_number)
        except Exception as e:
            print(e)
            print('文章推文數: ' + '0')
        time.sleep(3)

def getDataByID(targetID):
    idx=targetID
    print(idx)
    post_info = ptt_bot.get_post(
        Board,
        post_index=idx)
        #post_index=7486)

    try:
        print('---------------------------------')
        #print('Board: ' + post_info.board)
        #print('AID: ' + post_info.aid)
        print('index:' + str(post_info.index))
        #print('Author: ' + post_info.author)
        #print('Date: ' + post_info.date)
        print('Title: ' + post_info.title)
        print('List Date: ' + post_info.list_date)
        #print('content: ' + post_info.content)
        #print('Money: ' + str(post_info.money))
        #print('URL: ' + post_info.web_url)
        #print('IP: ' + post_info.ip)
        # 在文章列表上的日期
        #print('地區: ' + post_info.location)
        # Since 0.8.19
        # 有可能為 None，因為不是每篇文在文章列表都有推文數
        #print('文章推文數: ' + post_info.push_number)
        return post_info.title
    except Exception as e:
        print(e)
        print('文章推文數: ' + '0')
        return None



def getUserFinalID():
    global BoardLastID
    # need plus 1 for last one+1
    print('check board last id',BoardLastID)
    if BoardLastID==0:
        lastID=getBoardLastID()-10
        return lastID
    return BoardLastID+1
    #return 99895+1



#getDataBySearch()
#parseRangeDataByID()

def loopData():
    stockUserFinalID= getUserFinalID()
    stockBoardLastID = getBoardLastID()
    print(stockBoardLastID)
    if stockUserFinalID>stockBoardLastID:
        return
    for idx in range(stockUserFinalID, stockBoardLastID+1):
        d=getDataByID(idx)
        if d:
            print(d)
        else:
            print(f'{idx} not existed')
        time.sleep(3)

loopDelay=120
while True:
    loopData()
    time.sleep(loopDelay)


