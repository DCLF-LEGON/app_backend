from enum import Enum


class UserRoles(Enum):
    '''Defines the user roles in the system'''
    app_user = 'app_user'
    administrator = 'administrator'


class MediaType(Enum):
    '''Defines the media types'''
    audio = 'audio'
    video = 'video'
