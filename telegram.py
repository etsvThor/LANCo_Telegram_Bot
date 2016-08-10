#!/usr/bin/python
import telepot
import dateutil.parser
import time
import threading
import gcalender

TOKEN = '*********'
global TOKEN

#store in the speficiefed database if the text is not in de Database
def Store(text, Database):
    file = open("Database/"+Database,"r+")
    List = file.read().splitlines()
    if str(text) not in List:
            print("Storing the chat_id")
            file.write(str(text)+"\n")
            file.close()

#open the speficifed database and return its content
def Load(Database):
    file = open("Database/"+Database,"r+")
    List = file.read().splitlines()
    file.close()
    return List

def Update(Events,mode):
    if mode == 0:
        Notify(Events)
    if mode == 1:
        EventList = gcalender.main()
        ComputeText(EventList)
        Notify(EventList)
        # refresh calender and the text

    return


#Function that Notifys every chat about the upcoming event (from the Google calender)
def Notify(Events):
    print("Going to check if notifications need to be send")
    Chats = Load("Chats.db")
    localtime = time.localtime(time.time())
    LocalDate = [localtime[0], localtime[1], localtime[2], localtime[3]]
    for Event in Events:
        start = Event['start'].get('dateTime', Event['start'].get('date'))
        start = dateutil.parser.parse(start)
        EventDate = [int(start.strftime('%Y')), int(start.strftime('%-m')), int(start.strftime('%d')),int(start.strftime('%H')) ]

        #if the event day year and month are the same
        if EventDate[0] - LocalDate[0] == 0 and EventDate[1] - LocalDate[1] == 0 and EventDate[2] - LocalDate[2] == 0:

## Should also check at 24:00 !
            #if there is 1 hour between the local date and the event date
            if EventDate[3] - LocalDate[3] <= 1:
                msg = "This message is a kind reminder that " + Event['summary'] + " will start soon"
                msg = msg + "Therefore the organization of the TesLAN wants to urge you into getting your team ready and install everything you need "
                for w in Chats:
                    bot = YourBot(TOKEN)
                    bot.sendMessage(w, msg)


def Photos(PhotoName,chat_id):
    List = Load("Images.db")
    #http://stackoverflow.com/questions/10937918/loading-a-file-into-a-numpy-array-with-python
    print(List)
    PhotoNameList = List[0].split(";")
    print(PhotoNameList)
    bot = YourBot(TOKEN)
    if PhotoNameList in List:
        print("shortcut")
        FileId = PhotoName[1]
        bot.sendPhoto(chat_id,FileId)
        #list is not empty

    #send the photo by uploading it
    else:
        photo = open("Images/"+PhotoName,"rb")
        PhotoInfo = bot.sendPhoto(chat_id,photo)
        file_id = PhotoInfo['photo']
        file_id = file_id[4]
        file_id = file_id['file_id']
        StoreText = PhotoName + ";" + file_id
        Store(StoreText,"Images.db")

#function that computes the text that the bot uses
def ComputeText(Events):
    EventLists = Events
    global MsgText, InlineResponse, InfoText, PromoText, FaqText, EventLists

    def LineText():
        global MsgText, InfoText, PromoText,FaqText
        MsgText = "The games that will be played on  the TesLAN are : <strong> \n"
        for Event in Events:
            start = Event['start'].get('dateTime', Event['start'].get('date'))
            end = Event['end'].get('dateTime', Event['end'].get('date'))
            summary = Event['summary']
            # about = Event['description']
            start = dateutil.parser.parse(start)
            end = dateutil.parser.parse(end)
            MsgText = MsgText + "• " + summary + " which will be held from " + start.strftime('%d %A %I:%M ') + " till " + end.strftime('%d %A %I:%M') + "\n"
        MsgText = MsgText + "</strong>"
        file = open("Text/promo.md","r")
        PromoText = file.read()
        file.close()
        file = open("Text/info.md","r")
        InfoText = file.read()
        file.close()
        file = open("Text/faq.md", "r")
        FaqText = file.read()
        file.close()
        return MsgText,PromoText,FaqText,InfoText

    def InlineText(Events):
        InlineResponse = []
        id = 0
        global InlineResponse
        for Event in Events:
            start = Event['start'].get('dateTime', Event['start'].get('date'))
            end = Event['end'].get('dateTime', Event['end'].get('date'))
            title = Event['summary']
            url = Event['location'].split(";")
            start = dateutil.parser.parse(start)
            end = dateutil.parser.parse(end)
            about = Event['description']
            id = id +1
            SmallText = title + " will be held from " + start.strftime('%d %A %H:%M ') + " till " + end.strftime('%d %A %H:%M') + "\n"
            text = title + " will be held from " + start.strftime('%d %A %H:%M ') + " till " + end.strftime('%d %A %H:%M') + "\n \n" + about + "\n For more info please visit" + url[0]
            InlineResponse = InlineResponse + [{'type': 'article', 'id': str(id), 'title': title, 'message_text': text, 'url': url[0], 'thumb_url': url[1], 'description' :SmallText }]
        return InlineResponse

    LineText()
    InlineText(Events)

#would be fun to have a search function
def ComputedResponse(Input):
    print('Finding input')
    #print(InlineResponse)
    #print( re.search(Input,InlineResponse) )
    return InlineResponse


class YourBot(telepot.Bot):

    def __init__(self, *args, **kwargs):
        super(YourBot, self).__init__(*args, **kwargs)
        self._answerer = telepot.helper.Answerer(self)

    def on_chat_message(self, msg):
        #               0       1        2          3       4       5           6       7           8
        commands = ['/list', '/promo', '/date', '/faq', '/info', '/update', '/rules', '/games', '/poster']
        content_type, chat_type, chat_id = telepot.glance(msg)
        Store(chat_id,"Chats.db")
        commandtext = msg['text']
        command = commandtext.split("@")
        command = command[0]
        if command in commands:
            print('received a commando')
            if command == commands[0] or command == commands[2] or command == commands[7]:
                print('commando 0')
                self.sendMessage(chat_id, MsgText, "HTML")

            if command == commands[1]:
                print('commando 1')
                self.sendMessage(chat_id, PromoText, "Markdown")
            if command == commands[2]:
                print('commando 2')

            if command == commands[3]:
                print('commando 3')
                self.sendMessage(chat_id, FaqText, "Markdown")
            if command == commands[4]:
                print('commando 4')
                self.sendMessage(chat_id, InfoText, "Markdown")
            if command == commands[5]:
                print('commando 5')
                Update("placeholder", 1)
            if command == commands[6]:
                print('commando 6')

            if command == commands[7]:
                print('commando 7')
            #Poster
            if command == commands[8]:
                print('commando 8')
                Photos("poster.png",chat_id)
            #
            # if command == commands[9]:
            #     print('commando 9')
            #
            # if command == commands[10]:
            #     print('commando 10')

    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        print('Callback Query:', query_id, from_id, query_data)

    def on_inline_query(self, msg):
        query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
        print('Inline Query:', query_id, from_id, query_string)
        def compute():
            ans = ComputedResponse(query_string)
            return ans
        self._answerer.answer(msg, compute)

    def on_chosen_inline_result(self, msg):
        result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
        print('Chosen Inline Result:', result_id, from_id, query_string)


def main(Events):
    ComputeText(Events)
    Notify(Events)
    print('Starting the Telegram module')
#figure something clever for the secret Token
    bot = YourBot(TOKEN)
    bot.message_loop()
    #caal the update fucntion in a seperate thread every 3 minutes
    t = threading.Timer(300, Update, args=[Events,"0",] )
    t.start()
    print('Listening ...')
    while 1:
        time.sleep(10)




