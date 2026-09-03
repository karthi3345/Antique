import re

with open('templates/house/register.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add the phone number field before the submit button
phone_field = """
        <div class="field">
          <label for="id_phone">Phone Number:</label>
          <input type="tel" name="phone" id="id_phone" placeholder="+1 234 567 8900" required>
          <span class="helptext">For delivery and acquisition arrangements.</span>
        </div>
        
        <button type="submit" class="auth-submit">Create Account</button>"""

html = html.replace('<button type="submit" class="auth-submit">Create Account</button>', phone_field)

with open('templates/house/register.html', 'w', encoding='utf-8') as f:
    f.write(html)
