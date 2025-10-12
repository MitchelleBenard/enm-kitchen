from flask import Flask, render_template, request, redirect, url_for
import urllib.parse
import requests

app = Flask(__name__)

# WhatsApp setup
WHATSAPP_PHONE = "254113211652"  # your WhatsApp number (no +)
WHATSAPP_API_KEY = "YOUR_CALLMEBOT_API_KEY"  # replace with your actual API key from CallMeBot

@app.route("/")
def home():
    return render_template("order.html")

@app.route("/order", methods=["POST"])
def order():
    try:
        # Collect form data
        data = {
            "client": request.form.get("client"),
            "phone": request.form.get("phone"),
            "cake_flavour": request.form.get("cake_flavour"),
            "size": request.form.get("size"),
            "colour": request.form.get("colour"),
            "details": request.form.get("details"),
            "icing": request.form.get("icing"),
            "delivery": request.form.get("delivery"),
            "date": request.form.get("date"),
            "time": request.form.get("time"),
            "location": request.form.get("location"),
            "writings": request.form.get("writings"),
        }

        # Create WhatsApp message
        message = (
            f"🎂 *New ENM Kitchen Order!*\n\n"
            f"👤 Name: {data['client']}\n"
            f"📞 Phone: {data['phone']}\n"
            f"🍰 Flavour: {data['cake_flavour']}\n"
            f"📏 Size: {data['size']}\n"
            f"🎨 
            Colour: {data['colour']}\n"
            f"🧁 Icing: {data['icing']}\n"
            f"🚚 Delivery: {data['delivery']}\n"
            f"📅 Date: {data['date']}\n"
            f"⏰ Time: {data['time']}\n"
            f"📍 Location: {data['location']}\n"
            f"✍️ Writings: {data['writings']}\n"
            f"💬 Details: {data['details']}\n\n"
            f"📦 *Order received via ENM Kitchen Website.*"
        )

        # Encode and send to WhatsApp via CallMeBot API
        encoded_message = urllib.parse.quote_plus(message)
        api_url = f"https://api.callmebot.com/whatsapp.php?phone={WHATSAPP_PHONE}&text={encoded_message}&apikey={WHATSAPP_API_KEY}"

        response = requests.get(api_url, timeout=15)

        if response.status_code == 200:
            return redirect(url_for("thank_you"))
        else:
            return f"<h3>❌ Failed to send order. WhatsApp API error ({response.status_code})</h3>"

    except Exception as e:
        return f"<h3>⚠️ Error sending order: {e}</h3>"

@app.route("/thank-you")
def thank_you():
    return "<h2>✅ Order sent successfully to ENM Kitchen WhatsApp!</h2><a href='/'>Back to Home</a>"

if __name__ == "__main__":
    app.run(debug=True)
