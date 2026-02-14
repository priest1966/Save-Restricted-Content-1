#!/usr/bin/env python3
"""
Save Restricted Content Bot - MongoDB Version
Main Entry Point
"""

import os
import sys
import asyncio
import logging
import signal
from datetime import datetime
import plugins.handlers 
from pyrogram import Client, enums

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import API_ID, API_HASH, BOT_TOKEN, ADMINS, LOG_CHANNEL
from database.mongodb import init_db, close_db, db
from plugins.monitoring.cleanup import start_cleanup_scheduler
from plugins.monitoring.health import HealthMonitor
from plugins.monitoring.metrics import usage_stats
from plugins.services.session_manager import session_manager
from plugins.core.utils import setup_logging, get_logger

# Setup logging
setup_logging()
logger = get_logger(__name__)


class SaveRestrictedBot(Client):
    """Enhanced bot class with MongoDB backend"""
    
    def __init__(self):
        super().__init__(
            name="save_restricted_bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="plugins/handlers"),
            workers=20,
            sleep_threshold=10,
            max_concurrent_transmissions=3,
            ipv6=False,
            in_memory=True,
            parse_mode=enums.ParseMode.MARKDOWN
        )
        
        self.start_time = datetime.now()
        self.health_monitor = HealthMonitor(self)
        self.is_healthy = True
        
    async def start(self):
        """Start the bot with all services"""
        try:
            logger.info("🚀 Starting Save Restricted Bot (MongoDB Edition)...")
            
            # Initialize MongoDB connection
            await init_db()
            logger.info("✅ MongoDB connected successfully")
            
            # Start the client
            await super().start()
            
            # Get bot info
            self.me = await self.get_me()
            logger.info(f"✅ Bot started: @{self.me.username} (ID: {self.me.id})")
            
            # Start background tasks
            asyncio.create_task(start_cleanup_scheduler(self))
            asyncio.create_task(self.health_monitor.start_monitoring())
            
            # Resume pending queues
            from plugins.services.queue_manager import resume_all_queues
            await resume_all_queues(self)
            
            # Send startup notification
            # await self._send_startup_notification()
            
            logger.info(f"🎉 Bot started successfully! Uptime: {self.get_uptime()}")
            
        except Exception as e:
            logger.critical(f"❌ Failed to start bot: {e}", exc_info=True)
            raise
    
    async def stop(self, *args):
        """Stop the bot gracefully"""
        logger.info("🛑 Shutting down bot...")
        
        # Stop health monitor
        if self.health_monitor:
            await self.health_monitor.stop_monitoring()
        
        # Close all user sessions
        await session_manager.close_all_sessions()
        
        # Close MongoDB connection
        await close_db()
        
        # Stop client
        await super().stop()
        
        logger.info("👋 Bot stopped. Goodbye!")
    
    async def _send_startup_notification(self):
        """Send startup notification to admins"""
        if not ADMINS:
            return
        
        uptime = self.get_uptime()
        stats = usage_stats.get_summary()
        
        # Get MongoDB stats
        db_stats = await db.get_db_stats()
        collections = ", ".join(f"{k}: {v}" for k, v in db_stats.get("collections", {}).items())
        
        # Get user/session stats from DB
        total_users = await db.total_users_count()
        active_users = await db.get_active_users_count()
        active_sessions = len(await db.get_active_sessions())
        
        message = (
            f"✅ **Bot Started Successfully!**\n\n"
            f"🤖 **Bot:** @{self.me.username}\n"
            f"🆔 **ID:** `{self.me.id}`\n"
            f"⏱️ **Uptime:** {uptime}\n\n"
            f"📊 **MongoDB Status:**\n"
            f"• Database: `{db_stats.get('database', 'N/A')}`\n"
            f"• Collections: {collections}\n"
            f"• Data Size: `{humanbytes(db_stats.get('data_size', 0))}`\n\n"
            f"📈 **Bot Stats:**\n"
            f"• Total Users: {total_users}\n"
            f"• Active Users: {active_users}\n"
            f"• Active Sessions: {active_sessions}\n"
            f"• Total Downloads: {stats['total_downloads']}\n\n"
            f"📅 **Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        for admin_id in ADMINS:
            try:
                await self.send_message(admin_id, message)
                logger.info(f"📨 Startup notification sent to admin {admin_id}")
            except Exception as e:
                logger.error(f"Failed to notify admin {admin_id}: {e}")
        
        if LOG_CHANNEL:
            try:
                await self.send_message(int(LOG_CHANNEL), message)
            except:
                pass
    
    def get_uptime(self) -> str:
        """Get formatted uptime string"""
        delta = datetime.now() - self.start_time
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        parts.append(f"{seconds}s")
        
        return " ".join(parts)


def humanbytes(size: float) -> str:
    """Convert bytes to human readable format"""
    if not size:
        return "0 B"
    power = 2**10
    n = 0
    dic_power_n = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size > power:
        size /= power
        n += 1
    return f"{size:.2f} {dic_power_n[n]}"


def main():
    """Main entry point"""
    # Set up asyncio event loop policy for Windows
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    bot = None
    try:
        # Create and start bot
        bot = SaveRestrictedBot()
        
        # Run the bot
        bot.run()
        
    except KeyboardInterrupt:
        logger.info("👋 Received keyboard interrupt")
    except Exception as e:
        logger.critical(f"💥 Fatal error: {e}", exc_info=True)
    finally:
        if bot:
            try:
                if bot.is_connected:
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(bot.stop())
            except ConnectionError:
                pass
            except Exception as e:
                logger.error(f"Error stopping bot: {e}")
        logger.info("🏁 Bot process ended")


if __name__ == "__main__":
    main()