import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

class WalletBot:
    message = None
    bot = None
    bot_token = "BOT_TOKEN
    payload = False
    function = None
    payload_values = []

    def __init__(self):
        self.bot = telepot.Bot(self.bot_token)
        MessageLoop(self.bot, self.message_handler).run_as_thread()

    def message_handler(self, msg): 
        command = None
        request_type = None
        request_resource = None
        request_value = None

        if msg.get('data'): # Checks if is a inline response
            command = msg['data'].split("_")
            self.bot.deleteMessage((msg['message']['chat']['id'], msg['message']['message_id']))
        elif msg.get('text'): # Checks if is a text response
            command = msg['text'].split("_")
            if command[0] != '/start':
                self.bot.deleteMessage((msg['chat']['id'], msg['message_id']))
        else:
            print("Unable to obtain clear message")
        self.message = command

    def listen(self):
        while True:
            if self.message == None:
                pass
            else:
                print(self.message)
                self.logic()
                self.message = None
            pass


    def hello(self):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Wallet", callback_data="options_wallet")],
            [InlineKeyboardButton(text="Movements", callback_data="options_movements")],
        ])
        self.bot.sendMessage(936203322, 'Greetings, what do you wish to do: ', reply_markup = keyboard)

    def options_wallet(self):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Check Balance", callback_data="GET_wallet")],
            [InlineKeyboardButton(text="Create Wallet", callback_data="POST_wallet")],
            [InlineKeyboardButton(text="Update Wallet", callback_data="PUT_wallet")],
            [InlineKeyboardButton(text="Delete Wallet", callback_data="DELETE_wallet")],
        ])
        self.bot.sendMessage(936203322, '[Wallet] Pick an option: ', reply_markup = keyboard)

    def options_movements(self):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Check Movements", callback_data="GET_movements")],
            [InlineKeyboardButton(text="Create Movements", callback_data="POST_movements")],
            [InlineKeyboardButton(text="Update Movements", callback_data="PUT_movements")],
            [InlineKeyboardButton(text="Delete Movements", callback_data="DELETE_movements")],
        ])
        self.bot.sendMessage(936203322, '[Movements] Pick an option: ', reply_markup = keyboard)


    def create_payload(self):
        #==================GET==================
        #get wallet by id and all with 0
        if function = "GET_wallet":
            result = db.get_wallet(self.message[0])
            self.request = None
            self.bot.sendMessage(936203322, result)

        #get movement by id and all with 0
        if function = "GET_movement":
            result = db.get_wallet(self.message[0])
            self.request = None
            self.bot.sendMessage(936203322, result)      

        #==================POST==================
        if function = "POST_wallet":
            if len(self.array_payload) == 0:
                self.array_payload["name"] = self.message[0]
                self.bot.sendMessage(936203322, 'Insert the starting value!')
                
            elif len(self.array_payload) == 1:
                self.array_payload["value"] = self.message[0]
                db.post_wallet(payload)
                array_payload = []

        if function = "POST_movement":
            if len(self.array_payload) == 0:
                self.array_payload["type"] = self.message[0]
                self.bot.sendMessage(936203322, 'Insert the value!')
                
            elif len(self.array_payload) == 1:
                self.array_payload["value"] = self.message[0]
                self.bot.sendMessage(936203322, 'Insert the wallet!')

            elif len(self.array_payload) == 2:
                self.array_payload["wallet_id"] = self.message[0]
                db.post_movement(payload)
                array_payload = []            

        #==================DELETE==================
        if function = "DELETE_wallet":
            result = db.delete_wallet(self.message[0])
            self.request = None
            self.bot.sendMessage(936203322, result)

        if function = "DELETE_movement":
            result = db.delete_wallet(self.message[0])
            self.request = None
            self.bot.sendMessage(936203322, result)  

    def logic(self):
        if self.function != None:
            create_payload()

        if len(self.message) == 1:
            if self.message[0] == 'Hello':
                self.hello()
                return True

        if len(self.message) == 2:
            #==================OPTIONS==================
            if self.message[0] == 'options' and self.message[1] == 'wallet': 
                self.options_wallet()

            if self.message[0] == 'options' and self.message[1] == 'movements':
                self.options_movements()

            #==================GET==================
            if self.message[0] == 'GET' and self.message[1] == 'wallet':
                self.bot.sendMessage(936203322, 'Insert the ID of the wallet! (0 for all wallets)')
                self.function = "GET_wallet"


            if self.message[0] == 'GET' and self.message[1] == 'movement':
                self.bot.sendMessage(936203322, 'Insert the ID of the movement! (0 for all movements)')
                self.function = "GET_movement"

            #==================POST==================
            if self.message[0] == 'POST' and self.message[1] == 'wallet':
                self.bot.sendMessage(936203322, 'Insert the name of the wallet! (0 for all wallets)')
                self.function = "POST_wallet"

            if self.message[0] == 'POST' and self.message[1] == 'movement':
                self.bot.sendMessage(936203322, 'Insert the type of the movement! (0 for all wallets)')
                self.function = "POST_movement"

            #==================DELETE==================
            if self.message[0] == 'DELETE' and self.message[1] == 'wallet':
                self.bot.sendMessage(936203322, 'Insert the ID of the wallet!')
                self.function = "DELETE_wallet"

            if self.message[0] == 'DELETE' and self.message[1] == 'movements':
                self.bot.sendMessage(936203322, 'Insert the ID of the movement!')
                self.function = "DELETE_movement"
