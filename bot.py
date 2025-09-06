from telethon import TelegramClient, functions, events, types
from datetime import datetime, timedelta
import pytz
import asyncio

#tehran timezone
tehran_tz = pytz.timezone('Asia/Tehran')
#init client
client = TelegramClient("kopp", 00000, "api_hash")

peer_to = None
msgid_to = None


@client.on(events.NewMessage(outgoing=True))
async def set_vars(event):
    """reacts to some messages as commands for further functionality"""
    global peer_to, msgid_to
    message = event.message.message
    parts = message.split()
    if parts[0] == "setp" and len(parts) == 3:
        peer_to = parts[1]
        msgid_to = int(parts[2])
    if parts[0] == "settime" and len(parts) == 2:
        timess = parts[1]  # proper HH:MM:SS string
        await run_at_tehran_time(timess, the_task)
        await event.reply(f"The buying process will run at: {timess}")







async def create_invoice(peer, msgid):
    """automatically creates an invoice (telegram stars is the currency)"""
    entity = await client.get_input_entity(peer)
    return types.InputInvoiceMessage(
        peer=entity,
        msg_id=msgid,
    )


async def the_task():
    """this function does the main operation which is getting the payment form and sending it (buying the form)"""
    form = await client(functions.payments.GetPaymentFormRequest(
        invoice=await create_invoice(peer_to, msgid_to),
    ))
    result = await client(functions.payments.SendStarsFormRequest(
        form_id=form.form_id,
        invoice=await create_invoice(peer_to, msgid_to),
    ))
    await client(functions.messages.SendMessageRequest(
        peer="me",
        message=str(result)
    ))

async def run_at_tehran_time(timestr: str, action):
    """
    this function runs the "the_task" function at the given time (tehran time)
    timestr: string in HH:MM:SS format (Tehran time)
    action: function to execute
    """
    now = datetime.now(tehran_tz)

    # Parse input time string
    target_time = datetime.strptime(timestr, "%H:%M:%S").time()

    # Build full datetime for today with that time
    target = now.replace(hour=target_time.hour,
                         minute=target_time.minute,
                         second=target_time.second,
                         microsecond=0)

    # If the time already passed today, schedule for tomorrow
    if target <= now:
        target += timedelta(days=1)

    # Calculate wait seconds
    wait_seconds = (target - now).total_seconds()

    print(f"Waiting {wait_seconds:.2f} seconds until {target.strftime('%Y-%m-%d %H:%M:%S')} Tehran time...")
    await asyncio.sleep(wait_seconds)

    # Run the function
    asyncio.create_task(action())
#start the client
client.run_until_disconnected()
