from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_add = KeyboardButton(text='Add')
button_addforeign = KeyboardButton(text="Add foreign")
button_aq = KeyboardButton(text="Authors & Contributing")
button_back = KeyboardButton(text='Back')
button_cards = KeyboardButton(text="Cards")
button_configure = KeyboardButton(text="Configure")
button_createown = KeyboardButton(text="Create own")
button_delete = KeyboardButton(text="Delete")
button_description = KeyboardButton(text='Description')
button_edit = KeyboardButton(text="Edit cards")
button_faq = KeyboardButton(text="FAQ")
button_import = KeyboardButton(text='Import')
button_menu = KeyboardButton(text="Menu")
button_mycards = KeyboardButton(text="My cards")
button_name = KeyboardButton(text='Name')
button_order = KeyboardButton(text='Order')
button_play = KeyboardButton(text="Play")
button_random = KeyboardButton(text='Random')
button_remove = KeyboardButton(text='Remove')
button_reversed = KeyboardButton(text='Reversed')
button_show = KeyboardButton(text='Show')
button_straight = KeyboardButton(text='Straight')
button_sure = KeyboardButton(text="Sure")
button_unsure = KeyboardButton(text="Unsure")

kb_menu = ReplyKeyboardMarkup(resize_keyboard=True)
kb_menu.add(button_cards,
            button_faq,
            button_aq)

kb_have_cards = ReplyKeyboardMarkup(resize_keyboard=True)
kb_have_cards.add(button_mycards,
                  button_createown,
                  button_addforeign,
                  button_menu)

kb_dont_have_cards = ReplyKeyboardMarkup(resize_keyboard=True)
kb_dont_have_cards.add(button_createown,
                       button_addforeign,
                       button_menu)

kb_cancel = ReplyKeyboardMarkup(resize_keyboard=True)
kb_cancel.add(button_menu)

kb_back = ReplyKeyboardMarkup(resize_keyboard=True)
kb_back.add(button_back)

kb_deckcreated = ReplyKeyboardMarkup(resize_keyboard=True)
kb_deckcreated.add(button_edit,
                   button_cards,
                   button_menu)

kb_deckactions = ReplyKeyboardMarkup(resize_keyboard=True)
kb_deckactions.add(button_play,
                   button_edit,
                   button_configure,
                   button_delete,
                   button_menu)

kb_sure = ReplyKeyboardMarkup(resize_keyboard=True)
kb_sure.add(button_sure,
            button_unsure,
            button_menu)

kb_configuring = ReplyKeyboardMarkup(resize_keyboard=True)
kb_configuring.add(button_name,
                   button_description,
                   button_order,
                   button_back,
                   button_menu)

kb_order = ReplyKeyboardMarkup(resize_keyboard=True)
kb_order.add(button_straight,
             button_reversed,
             button_random,
             button_back,
             button_menu)

kb_editing = ReplyKeyboardMarkup(resize_keyboard=True)
kb_editing.add(button_show,
               button_add,
               button_remove,
               button_import,
               button_back,
               button_menu)
