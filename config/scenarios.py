def get_premade_scenarios():
    scenarios = [
            {
                "email": """From: service@amaz0n.com
Subject: Urgent: Your Account Has Been Compromised
                
Dear Valued Customer,
                
We have detected suspicious activity on your account. Your account has been temporarily suspended.
                
Please click the link below to verify your information and restore your account:
http://amazonn-secure.com/verify
                
If you don't respond within 24 hours, your account will be permanently closed.
                
Amazon Security Team""",
                "is_phishing": True,
                "explanation": """This is a phishing attempt! Here are the red flags:
1. The sender's email contains a zero instead of an 'o' (amaz0n.com)
2. The link domain is misspelled (amazonn-secure.com)
3. The message creates urgency with threats of account closure
4. It asks you to click a suspicious link
5. It doesn't address you by name"""
            },
            {
                "email": """From: newsletter@spotify.com
Subject: Your Monthly Spotify Recap
                
Hi there,
                
Here's your monthly listening summary:
- You listened to 427 minutes of music this month
- Your top artist was The Weeknd
- Your favorite genre was Pop
                
Check out your personalized playlist based on your listening habits:
https://open.spotify.com/playlist/recommendations
                
Enjoy the music!
The Spotify Team""",
                "is_phishing": False,
                "explanation": """This is legitimate! Here's why:
1. The sender's email is from the correct domain (spotify.com)
2. The content is personalized based on your listening habits
3. The link goes to the official Spotify domain
4. There's no urgency or threats
5. It doesn't ask for personal information"""
            },
            {
                "email": """From: paypal-security@paypal-team.com
Subject: PayPal: Confirm Your Recent Transaction
                
Dear PayPal User,
                
We've detected a unusual transaction on your account for $750.00 to "Online Electronics Store".
                
If you did not make this transaction, you must immediate verify your account details by clicking the link below:
                
https://paypal-secure-center.com/verify
                
Your account will be locked if you do not respond within 12 hours.
                
Security Department
PayPal""",
                "is_phishing": True,
                "explanation": """This is a phishing attempt! Here are the red flags:
1. The sender's email is not from the official PayPal domain (paypal.com)
2. The domain "paypal-team.com" is suspicious
3. The verification link goes to an unofficial website
4. There are grammar errors ("a unusual transaction", "immediate verify")
5. The message creates urgency with a time limit
6. It doesn't address you by name"""
            },
            {
                "email": """From: no-reply@linkedin.com
Subject: John Smith has sent you a connection request
                
LinkedIn
                
John Smith has sent you a connection request
                
I'd like to add you to my professional network on LinkedIn.
- John Smith, Senior Developer at Tech Solutions Inc.
                
[View profile]
                
You are receiving connection requests emails. Unsubscribe here.
                
© 2023 LinkedIn Corporation, 1000 W Maude Ave, Sunnyvale, CA 94085.""",
                "is_phishing": False,
                "explanation": """This is legitimate! Here's why:
1. The sender's email is from the correct domain (linkedin.com)
2. The format matches standard LinkedIn connection requests
3. The message is specific about who sent the request
4. It includes a normal LinkedIn footer with unsubscribe option
5. There's no urgency or threats
6. It doesn't ask for sensitive information"""
            },
            {
                "email": """From: microsoftsupport@outlook-team.com
Subject: Your Microsoft 365 subscription is expiring
                
MICROSOFT 365
                
Dear Customer,
                
Your Microsoft 365 subscription will expire in 2 days. To ensure no disruption to your service, please update your payment details urgently.
                
Click here to update your payment information: https://microsoft365-renewal.com
                
Note: Failure to update will result in immediate service termination.
                
Microsoft Support Team""",
                "is_phishing": True,
                "explanation": """This is a phishing attempt! Here are the red flags:
1. The sender's email is not from Microsoft's official domain
2. The domain "outlook-team.com" is suspicious
3. The link goes to an unofficial website
4. The message creates urgency
5. It doesn't address you by name
6. Microsoft typically sends subscription reminders well in advance"""
            },
            {
                "email": """From: noreply@netflix.com
Subject: Your Netflix bill
                
Your monthly Netflix subscription has been processed.
                
Billing date: April 3, 2023
Amount: $14.99
Next billing date: May 3, 2023
                
To view your receipt, visit netflix.com/YourAccount
                
Questions? Visit the Help Center: help.netflix.com
                
Netflix""",
                "is_phishing": False,
                "explanation": """This is legitimate! Here's why:
1. The sender's email is from the correct domain (netflix.com)
2. It's a standard billing notification with specific details
3. The message directs you to the official Netflix website
4. There's no urgency or threats
5. It doesn't ask you to click suspicious links
6. It offers legitimate help resources"""
            },
            {
                "email": """From: support@applesecure.net
Subject: Apple ID: Your account has been locked
                
Dear Customer,
                
Your Apple ID has been locked due to too many failed login attempts.
                
To unlock your account, please verify your information by clicking on the link below:
                
https://apple-id-unlock.com/verify
                
If you don't verify within 24 hours, your account will be permanently deleted.
                
Apple Support""",
                "is_phishing": True,
                "explanation": """This is a phishing attempt! Here are the red flags:
1. The sender's email is not from Apple's official domain (apple.com)
2. The domain "applesecure.net" is suspicious
3. The verification link goes to an unofficial website
4. The message creates urgency with threats of account deletion
5. It doesn't address you by name
6. Apple never threatens to delete accounts in this manner"""
            },
            {
                "email": """From: billing@amazon.com
Subject: Your Amazon.com order #112-7366937-2795436
                
Hello Rachel,
                
Thank you for your order. Your Amazon.com order #112-7366937-2795436 has shipped.
                
Your package was sent to:
Rachel Johnson
123 Main Street
Springfield, IL 62704
                
You can track your package at: amazon.com/your-orders
                
Order Details:
1x Book: "The Psychology of Money" - $15.99
                
Thank you for shopping with us.
Amazon.com""",
                "is_phishing": False,
                "explanation": """This is legitimate! Here's why:
1. The sender's email is from the correct domain (amazon.com)
2. It includes specific order details with a genuine-looking order number
3. It addresses the recipient by name
4. The tracking link directs to the official Amazon website
5. The message is informational with no urgency or threats
6. It doesn't ask for sensitive information"""
            },
            {
                "email": """From: service@bankofamerica-secure.com
Subject: URGENT: Unusual activity detected on your account
                
BANK OF AMERICA
                
Dear Client,
                
We have detected unusual activity on your account. For your security, we have limited access to your online banking.
                
CLICK HERE TO VERIFY YOUR IDENTITY AND RESTORE ACCESS
                
If we don't hear from you within 24 hours, your account will remain restricted.
                
Bank of America Security Team""",
                "is_phishing": True,
                "explanation": """This is a phishing attempt! Here are the red flags:
1. The sender's email is not from Bank of America's official domain
2. The domain "bankofamerica-secure.com" is suspicious
3. The "CLICK HERE" doesn't show the actual URL
4. The message creates urgency with threats of continued restriction
5. It doesn't address you by name
6. Banks typically don't send emails with "CLICK HERE" buttons for security issues"""
            },
            {
                "email": """From: no-reply@dropbox.com
Subject: John shared "Project Proposal" with you
                
Dropbox
                
John Smith (john.smith@company.com) shared "Project Proposal" with you
                
View file
                
The link to view this file will expire in 30 days.
                
Need help? Visit the Dropbox Help Center.
                
© 2023 Dropbox""",
                "is_phishing": False,
                "explanation": """This is legitimate! Here's why:
1. The sender's email is from the correct domain (dropbox.com)
2. The format matches standard Dropbox file sharing notifications
3. It includes specific details about who shared what
4. It mentions a reasonable expiration period for the link
5. It directs to legitimate help resources
6. There's no urgency or threats"""
            },
            {
                "email": """From: security@apple.com
Subject: Important: Update Your Apple ID Password
                
Dear Apple User,
                
We have noticed suspicious login attempts on your Apple ID. Please update your password immediately to secure your account.
                
Click here to update your password: https://appleid.apple.com
                
Thank you,
Apple Security Team""",
                "is_phishing": False,
                "explanation": """This is legitimate! Here's why:
1. The sender's email is from the official Apple domain (apple.com)
2. The link directs to the official Apple website
3. The message is polite and informative without creating undue urgency
4. It does not ask for personal details directly in the email
5. It addresses the user generally, which is common for security alerts"""
            },
            {
                "email": """From: support@freegiftcards.com
Subject: Congratulations! You've won a $500 gift card
                
Dear Winner,
                
You have been selected to receive a $500 gift card! Click the link below to claim your prize:
http://freegiftcards-claim.com
                
Hurry, offer expires soon!""",
                "is_phishing": True,
                "explanation": """This is a phishing attempt! Here are the red flags:
1. The sender's email is from a suspicious domain (freegiftcards.com)
2. The message promises unrealistic rewards
3. The link directs to an unofficial and suspicious website
4. The message creates urgency to rush the user
5. It does not address the recipient by name"""
            },
            {
                "email": """From: updates@github.com
Subject: Security Alert: New sign-in to your GitHub account
                
Hi David,
                
We detected a new sign-in to your GitHub account from a new device.
                
If this was you, no further action is needed.
If you did not sign in, please secure your account immediately:
https://github.com/settings/security
                
GitHub Security Team""",
                "is_phishing": False,
                "explanation": """This is legitimate! Here's why:
1. The sender's email is from the official GitHub domain
2. The email addresses the user by name
3. The link directs to the official GitHub website
4. The message is informative and non-threatening
5. It includes clear instructions for securing the account if needed"""
            },
            {
                "email": """From: billing@paypal.com
Subject: Your PayPal invoice #INV-123456
                
Hello,
                
Your PayPal invoice #INV-123456 for $120.00 has been generated.
                
You can view and pay your invoice here:
https://www.paypal.com/invoice/p/#INV-123456
                
Thank you for using PayPal.""",
                "is_phishing": False,
                "explanation": """This is legitimate! Here's why:
1. The sender's email is from the official PayPal domain
2. The invoice number is specific and realistic
3. The link directs to the official PayPal website
4. The message is formal and informational
5. There is no urgency or request for personal information"""
            },
            {
                "email": """From: admin@secure-bank.com
Subject: Account Suspension Notice
                
Dear Customer,
                
Your bank account has been suspended due to suspicious activity.
Please verify your identity immediately by clicking the link below:
http://secure-bank-verification.com
                
Failure to comply within 24 hours will result in permanent suspension.
                
Thank you,
Secure Bank""",
                "is_phishing": True,
                "explanation": """This is a phishing attempt! Here are the red flags:
1. The sender's email domain is suspicious and not official
2. The link directs to an unofficial website
3. The message creates urgency and threats of suspension
4. It does not address the recipient by name
5. Banks usually do not ask for verification via email links"""
            },
            {
                "email": """From: notifications@twitter.com
Subject: New login from Chrome on Windows
                
Hi David,
                
We noticed a new login to your Twitter account from Chrome on Windows.
If this was you, you can disregard this message.
If not, please secure your account immediately:
https://twitter.com/account/access
                
Thanks,
Twitter Security""",
                "is_phishing": False,
                "explanation": """This is legitimate! Here's why:
1. The sender's email is from the official Twitter domain
2. The email addresses the user by name
3. The link directs to the official Twitter website
4. The message is informative and non-threatening
5. It provides clear instructions if the login was unauthorized"""
            },
            {
                "email": """From: support@windowsupdate.com
Subject: Critical Windows Update Required
                
Dear User,
                
Your computer is at risk. Please download the latest critical update immediately:
http://windowsupdate-secure.com/download
                
Failure to update will compromise your system security.
                
Windows Update Team""",
                "is_phishing": True,
                "explanation": """This is a phishing attempt! Here are the red flags:
1. The sender's email domain is not official (windowsupdate.com is suspicious)
2. The link directs to an unofficial website
3. The message creates undue urgency and fear
4. It asks for immediate action via link download
5. Microsoft does not send update links via email"""
            },
            {
                "email": """From: contact@etsy.com
Subject: Your Etsy order has shipped
                
Hello Sarah,
                
Good news! Your Etsy order #987654321 has shipped.
You can track your package here:
https://www.etsy.com/your/receipts
                
Thank you for shopping with Etsy!""",
                "is_phishing": False,
                "explanation": """This is legitimate! Here's why:
1. The sender's email is from the official Etsy domain
2. The email addresses the recipient by name
3. The link directs to the official Etsy website
4. The message is informative and non-threatening
5. It includes specific order details"""
            },
            {
                "email": """From: admin@secure-paypal.com
Subject: PayPal Account Locked
                
Dear User,
                
Your PayPal account has been locked due to suspicious activity.
Please verify your account details immediately:
http://secure-paypal.com/verify
                
If you don't respond within 24 hours, your account will be permanently suspended.
                
PayPal Security Team""",
                "is_phishing": True,
                "explanation": """This is a phishing attempt! Here are the red flags:
1. The sender's email domain is not official (secure-paypal.com)
2. The link directs to an unofficial website
3. The message creates urgency and threats of suspension
4. It does not address the recipient by name
5. PayPal does not ask for verification via email links"""
            }
    ]
    return scenarios