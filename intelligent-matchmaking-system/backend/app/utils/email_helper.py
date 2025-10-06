"""
Email helper utilities for sending notifications and communications
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class EmailHelper:
    def __init__(self):
        self.smtp_host = settings.email_host
        self.smtp_port = settings.email_port
        self.username = settings.email_username
        self.password = settings.email_password
        self.is_configured = all([self.smtp_host, self.smtp_port, self.username, self.password])
    
    async def send_welcome_email(self, to_email: str, username: str) -> bool:
        """Send welcome email to new user"""
        subject = f"Welcome to {settings.app_name}!"
        
        html_content = f"""
        <html>
        <body>
            <h2>Welcome to {settings.app_name}, {username}!</h2>
            <p>Thank you for joining our intelligent matchmaking community for peer-assisted learning.</p>
            
            <h3>Get Started:</h3>
            <ul>
                <li>Complete your profile to get better matches</li>
                <li>Add your learning interests and strengths</li>
                <li>Start exploring potential study partners</li>
                <li>Join study groups in your field</li>
            </ul>
            
            <p>We're excited to help you on your learning journey!</p>
            
            <p>Best regards,<br>
            The {settings.app_name} Team</p>
        </body>
        </html>
        """
        
        return await self._send_email(to_email, subject, html_content)
    
    async def send_match_notification(self, to_email: str, username: str, match_details: dict) -> bool:
        """Send notification about new match"""
        subject = "New Study Partner Match Found!"
        
        html_content = f"""
        <html>
        <body>
            <h2>Great news, {username}!</h2>
            <p>We found a potential study partner for you.</p>
            
            <h3>Match Details:</h3>
            <ul>
                <li><strong>Partner:</strong> {match_details.get('partner_name', 'N/A')}</li>
                <li><strong>Compatibility Score:</strong> {match_details.get('compatibility_score', 0):.0%}</li>
                <li><strong>Common Topics:</strong> {', '.join(match_details.get('topics', []))}</li>
                <li><strong>Academic Level:</strong> {match_details.get('academic_level', 'N/A')}</li>
            </ul>
            
            <p>Log in to your dashboard to review this match and send a connection request.</p>
            
            <p>Happy learning!<br>
            The {settings.app_name} Team</p>
        </body>
        </html>
        """
        
        return await self._send_email(to_email, subject, html_content)
    
    async def send_session_reminder(self, to_email: str, username: str, session_details: dict) -> bool:
        """Send reminder about upcoming study session"""
        subject = "Study Session Reminder"
        
        html_content = f"""
        <html>
        <body>
            <h2>Session Reminder for {username}</h2>
            <p>You have an upcoming study session scheduled.</p>
            
            <h3>Session Details:</h3>
            <ul>
                <li><strong>Topic:</strong> {session_details.get('topic', 'N/A')}</li>
                <li><strong>Date & Time:</strong> {session_details.get('scheduled_time', 'N/A')}</li>
                <li><strong>Duration:</strong> {session_details.get('duration', 60)} minutes</li>
                <li><strong>Location:</strong> {session_details.get('location', 'Online')}</li>
                <li><strong>Partner:</strong> {session_details.get('partner_name', 'N/A')}</li>
            </ul>
            
            <p>Don't forget to prepare any materials you might need for the session.</p>
            
            <p>Good luck with your session!<br>
            The {settings.app_name} Team</p>
        </body>
        </html>
        """
        
        return await self._send_email(to_email, subject, html_content)
    
    async def send_feedback_request(self, to_email: str, username: str, session_details: dict) -> bool:
        """Send request for session feedback"""
        subject = "Please Share Your Session Feedback"
        
        html_content = f"""
        <html>
        <body>
            <h2>How was your study session, {username}?</h2>
            <p>We hope you had a productive learning experience!</p>
            
            <h3>Session Details:</h3>
            <ul>
                <li><strong>Topic:</strong> {session_details.get('topic', 'N/A')}</li>
                <li><strong>Partner:</strong> {session_details.get('partner_name', 'N/A')}</li>
                <li><strong>Date:</strong> {session_details.get('date', 'N/A')}</li>
            </ul>
            
            <p>Your feedback helps us improve our matching algorithm and helps your study partner grow.</p>
            
            <p><strong>Please take 2 minutes to rate your session and provide feedback.</strong></p>
            
            <p>Thank you for being part of our learning community!<br>
            The {settings.app_name} Team</p>
        </body>
        </html>
        """
        
        return await self._send_email(to_email, subject, html_content)
    
    async def send_achievement_notification(self, to_email: str, username: str, achievement: dict) -> bool:
        """Send notification about new achievement/badge"""
        subject = f"🎉 New Achievement Unlocked: {achievement.get('name', 'Achievement')}"
        
        html_content = f"""
        <html>
        <body>
            <h2>Congratulations, {username}! 🎉</h2>
            <p>You've unlocked a new achievement!</p>
            
            <h3>🏆 {achievement.get('name', 'Achievement')}</h3>
            <p><em>{achievement.get('description', 'Great job!')}</em></p>
            
            <h3>Reward:</h3>
            <ul>
                <li><strong>Points Earned:</strong> +{achievement.get('points', 0)}</li>
                <li><strong>Badge:</strong> {achievement.get('badge_name', 'Special Badge')}</li>
            </ul>
            
            <p>Keep up the excellent work in your learning journey!</p>
            
            <p>Best regards,<br>
            The {settings.app_name} Team</p>
        </body>
        </html>
        """
        
        return await self._send_email(to_email, subject, html_content)
    
    async def send_weekly_summary(self, to_email: str, username: str, summary: dict) -> bool:
        """Send weekly learning summary"""
        subject = f"Your Weekly Learning Summary - {settings.app_name}"
        
        html_content = f"""
        <html>
        <body>
            <h2>Weekly Summary for {username}</h2>
            <p>Here's what you accomplished this week:</p>
            
            <h3>📊 Learning Statistics:</h3>
            <ul>
                <li><strong>Study Sessions:</strong> {summary.get('sessions_count', 0)}</li>
                <li><strong>Total Study Time:</strong> {summary.get('total_time', 0)} minutes</li>
                <li><strong>Topics Covered:</strong> {summary.get('topics_count', 0)}</li>
                <li><strong>Points Earned:</strong> +{summary.get('points_earned', 0)}</li>
            </ul>
            
            <h3>🎯 This Week's Highlights:</h3>
            <ul>
                {self._format_highlights(summary.get('highlights', []))}
            </ul>
            
            <h3>📈 Goals for Next Week:</h3>
            <ul>
                {self._format_goals(summary.get('suggested_goals', []))}
            </ul>
            
            <p>Keep up the momentum in your learning journey!</p>
            
            <p>Best regards,<br>
            The {settings.app_name} Team</p>
        </body>
        </html>
        """
        
        return await self._send_email(to_email, subject, html_content)
    
    async def send_password_reset(self, to_email: str, username: str, reset_token: str) -> bool:
        """Send password reset email"""
        subject = "Password Reset Request"
        
        # In a real implementation, this would include a proper reset link
        reset_link = f"https://yourapp.com/reset-password?token={reset_token}"
        
        html_content = f"""
        <html>
        <body>
            <h2>Password Reset Request</h2>
            <p>Hello {username},</p>
            
            <p>We received a request to reset your password for your {settings.app_name} account.</p>
            
            <p>If you made this request, click the link below to reset your password:</p>
            <p><a href="{reset_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Reset Password</a></p>
            
            <p>This link will expire in 24 hours for security reasons.</p>
            
            <p>If you didn't request this password reset, please ignore this email or contact support if you have concerns.</p>
            
            <p>Best regards,<br>
            The {settings.app_name} Team</p>
        </body>
        </html>
        """
        
        return await self._send_email(to_email, subject, html_content)
    
    async def _send_email(self, to_email: str, subject: str, html_content: str) -> bool:
        """Send email using SMTP"""
        if not self.is_configured:
            logger.warning("Email not configured. Email would be sent to: %s with subject: %s", to_email, subject)
            return False
        
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.username
            message["To"] = to_email
            
            # Add HTML content
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(message)
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False
    
    def _format_highlights(self, highlights: List[str]) -> str:
        """Format highlights as HTML list items"""
        if not highlights:
            return "<li>No highlights this week</li>"
        
        return "".join(f"<li>{highlight}</li>" for highlight in highlights)
    
    def _format_goals(self, goals: List[str]) -> str:
        """Format goals as HTML list items"""
        if not goals:
            return "<li>Continue your excellent progress!</li>"
        
        return "".join(f"<li>{goal}</li>" for goal in goals)


# Global instance
email_helper = EmailHelper()