'''
Author: Night-stars-1 nujj1042633805@gmail.com
Date: 2023-06-24 22:03:09
LastEditors: Night-stars-1 nujj1042633805@gmail.com
LastEditTime: 2023-06-25 15:27:44
Description: 

Copyright (c) 2023 by Night-stars-1, All Rights Reserved. 
'''
"""
### QQ好友相关
"""
import asyncio

from nonebot import get_driver, on_request
from nonebot.adapters.qqguild import Bot
from nonebot_plugin_apscheduler import scheduler

from .plugin_data import PluginDataManager, write_plugin_data
from .utils import logger

_conf = PluginDataManager.plugin_data_obj
_driver = get_driver()


@_driver.on_bot_connect
async def check_friend_list(bot: Bot):
    """
    检查用户是否仍在好友列表中，不在的话则删除
    """
    logger.info(f'{_conf.preference.log_head}正在检查好友列表...')
    friend_list = await bot.get_members(guild_id="17290119065657530577", after=0, limit=100)
    friend_list = [{"user_id": int(i.user.id)} for i in friend_list]
    user_list = _conf.users.copy()
    for user in user_list:
        user_filter = filter(lambda x: x["user_id"] == user, friend_list)
        friend = next(user_filter, None)
        if not friend:
            logger.info(f'{_conf.preference.log_head}用户 {user} 不在好友列表内，已删除其数据')
            _conf.users.pop(user)
            write_plugin_data()


@_driver.on_bot_connect
async def _(bot: Bot):
    scheduler.add_job(id='check_friend', replace_existing=True,
                      trigger="cron", hour='23', minute='59', func=check_friend_list, args=(bot,))
