"""
Notifier Module
Sends alerts via Email and Telegram
"""

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

try:
    import telegram
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    logging.warning("Telegram not installed")


class EmailNotifier:
    """Send notifications via Email"""
    
    def __init__(self, sender_email, sender_password, smtp_server='smtp.gmail.com', smtp_port=587):
        """
        Initialize Email Notifier
        
        Args:
            sender_email: Sender email address
            sender_password: Email password or app password
            smtp_server: SMTP server (default Gmail)
            smtp_port: SMTP port (default 587)
        """
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.logger = logging.getLogger(__name__)
    
    def send_email(self, recipient_email, subject, message):
        """
        Send email notification
        
        Args:
            recipient_email: Recipient email address
            subject: Email subject
            message: Email body
        
        Returns:
            True if successful, False otherwise
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            # Add timestamp to message
            body = f"{message}\n\n---\nSent: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            self.logger.info(f"Email sent to {recipient_email}: {subject}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending email: {e}")
            return False
    
    def send_trade_alert(self, recipient_email, trade_info):
        """Send trade execution alert"""
        subject = f"Trade Alert: {trade_info['side'].upper()} {trade_info['symbol']}"
        message = f"""
Trade Executed:
- Symbol: {trade_info['symbol']}
- Side: {trade_info['side'].upper()}
- Quantity: {trade_info['qty']}
- Price: ${trade_info['price']:.2f}
- Status: {trade_info['status']}
"""
        return self.send_email(recipient_email, subject, message)
    
    def send_alert(self, recipient_email, alert_type, details):
        """Send generic alert"""
        subject = f"Trading Bot Alert: {alert_type}"
        message = f"""
Alert Type: {alert_type}
Details: {details}
"""
        return self.send_email(recipient_email, subject, message)


class TelegramNotifier:
    """Send notifications via Telegram"""
    
    def __init__(self, bot_token, chat_id):
        """
        Initialize Telegram Notifier
        
        Args:
            bot_token: Telegram bot token
            chat_id: Telegram chat ID
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.logger = logging.getLogger(__name__)
        
        if TELEGRAM_AVAILABLE:
            try:
                self.bot = telegram.Bot(token=bot_token)
                self.logger.info("Telegram bot initialized")
            except Exception as e:
                self.logger.error(f"Error initializing Telegram bot: {e}")
                self.bot = None
        else:
            self.bot = None
            self.logger.warning("Telegram library not available")
    
    def send_message(self, message):
        """
        Send Telegram message
        
        Args:
            message: Message text
        
        Returns:
            True if successful, False otherwise
        """
        if not self.bot:
            self.logger.warning("Telegram bot not initialized")
            return False
        
        try:
            self.bot.send_message(chat_id=self.chat_id, text=message)
            self.logger.info("Telegram message sent")
            return True
        except Exception as e:
            self.logger.error(f"Error sending Telegram message: {e}")
            return False
    
    def send_trade_alert(self, trade_info):
        """Send trade execution alert"""
        message = f"""
🔔 Trade Alert
━━━━━━━━━━━━━━━━
Symbol: {trade_info['symbol']}
Side: {trade_info['side'].upper()}
Qty: {trade_info['qty']}
Price: ${trade_info['price']:.2f}
Status: {trade_info['status']}
Time: {datetime.now().strftime('%H:%M:%S')}
"""
        return self.send_message(message)
    
    def send_signal_alert(self, symbol, signal, confidence):
        """Send trading signal alert"""
        emoji = "📈" if signal == "bullish" else "📉"
        message = f"""
{emoji} Trading Signal
━━━━━━━━━━━━━━━━
Symbol: {symbol}
Signal: {signal.upper()}
Confidence: {confidence:.1%}
Time: {datetime.now().strftime('%H:%M:%S')}
"""
        return self.send_message(message)
    
    def send_risk_alert(self, alert_type, details):
        """Send risk management alert"""
        message = f"""
⚠️ Risk Alert
━━━━━━━━━━━━━━━━
Type: {alert_type}
Details: {details}
Time: {datetime.now().strftime('%H:%M:%S')}
"""
        return self.send_message(message)


class NotificationManager:
    """Manage multiple notification channels"""
    
    def __init__(self):
        """Initialize Notification Manager"""
        self.email_notifier = None
        self.telegram_notifier = None
        self.logger = logging.getLogger(__name__)
    
    def add_email_notifier(self, sender_email, sender_password, smtp_server='smtp.gmail.com'):
        """Add email notification channel"""
        self.email_notifier = EmailNotifier(sender_email, sender_password, smtp_server)
        self.logger.info("Email notifier added")
    
    def add_telegram_notifier(self, bot_token, chat_id):
        """Add Telegram notification channel"""
        self.telegram_notifier = TelegramNotifier(bot_token, chat_id)
        self.logger.info("Telegram notifier added")
    
    def send_trade_alert(self, trade_info, recipient_email=None):
        """Send trade alert on all channels"""
        if self.email_notifier and recipient_email:
            self.email_notifier.send_trade_alert(recipient_email, trade_info)
        
        if self.telegram_notifier:
            self.telegram_notifier.send_trade_alert(trade_info)
    
    def send_signal_alert(self, symbol, signal, confidence, recipient_email=None):
        """Send signal alert on all channels"""
        if self.email_notifier and recipient_email:
            message = f"Trading Signal: {symbol} - {signal.upper()} (Confidence: {confidence:.1%})"
            self.email_notifier.send_alert(recipient_email, "Trading Signal", message)
        
        if self.telegram_notifier:
            self.telegram_notifier.send_signal_alert(symbol, signal, confidence)
    
    def send_risk_alert(self, alert_type, details, recipient_email=None):
        """Send risk alert on all channels"""
        if self.email_notifier and recipient_email:
            self.email_notifier.send_alert(recipient_email, alert_type, details)
        
        if self.telegram_notifier:
            self.telegram_notifier.send_risk_alert(alert_type, details)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Example usage
    nm = NotificationManager()
    
    # Add email (requires Gmail app password)
    # nm.add_email_notifier('your_email@gmail.com', 'your_app_password')
    
    # Add Telegram (requires bot token and chat ID)
    # nm.add_telegram_notifier('YOUR_BOT_TOKEN', 'YOUR_CHAT_ID')
    
    # Send alerts
    trade_info = {
        'symbol': 'AAPL',
        'side': 'buy',
        'qty': 10,
        'price': 150.25,
        'status': 'filled'
    }
    
    # nm.send_trade_alert(trade_info, 'recipient@gmail.com')
    # nm.send_signal_alert('AAPL', 'bullish', 0.75, 'recipient@gmail.com')
    # nm.send_risk_alert('Stop Loss', 'AAPL hit stop loss at $145.00', 'recipient@gmail.com')
