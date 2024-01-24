import logging
import httpx
import aiogram.utils.markdown as md

from core.settings import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


async def get_last_threads():
    async with httpx.AsyncClient() as client:
        res = await client.post(
            f'https://api.skiff.com/graphql',
            headers = {
                'apollographql-client-name': 'skemail-web',
                'apollographql-client-version': '8d26b96c',
                'x-skiff-userid': settings.skiff_userid,
                'Cookie': f'__Secure-auth_cookie_{settings.skiff_userid}={settings.skiff_secure}',
                'User-Agent': 'Skiff2TG'
            },
            json=[
                {
                    "operationName": "mailbox",
                    "variables": {
                        "request": {
                            "label": "INBOX",
                            "cursor": None,
                            "limit": 20,
                            "filters": {},
                            "platformInfo": {
                                "isIos": False,
                                "isAndroid": False,
                                "isMacOs": False,
                                "isMobile": False,
                                "isReactNative": False,
                                "isSkiffWindowsDesktop": False
                            },
                            "isAliasInbox": False,
                            "clientsideFiltersApplied": True,
                            "refetching": True
                        }
                    },
                    "query": """
                        query mailbox($request: MailboxRequest!) {
                            mailbox(request: $request) {
                                threads {
                                    ...ThreadWithoutContent
                                }
                                pageInfo {
                                    hasNextPage
                                    cursor {
                                        threadID
                                        date
                                    }
                                }
                            }
                        }

                        fragment ThreadWithoutContent on UserThread {
                            threadID
                            attributes {
                                read
                                systemLabels
                                userLabels {
                                    labelID
                                    labelName
                                    variant
                                }
                                snoozedTo
                                snoozedAt
                            }
                            emails {
                                ...EmailWithoutContent
                            }
                            emailsUpdatedAt
                            sentLabelUpdatedAt
                            deletedAt
                        }

                        fragment EmailWithoutContent on Email {
                            id
                            attachmentMetadata {
                                attachmentID
                            }
                            createdAt
                            from {
                                ...Address
                            }
                            to {
                                ...Address
                            }
                            cc {
                                ...Address
                            }
                            bcc {
                                ...Address
                            }
                            replyTo {
                                ...Address
                            }
                            attachmentMetadata {
                                attachmentID
                            }
                            scheduleSendAt
                            notificationsTurnedOffForSender
                            pgpKeyIDs
                            pgpID
                            forwardedTo
                        }

                        fragment Address on AddressObject {
                            name
                            address
                            blocked
                        }
                    """
                }
            ]
        )
        if res.status_code != 200:
            logger.error(f'Failed request skiff.com with {res.status_code} code: {res.text}')
            return md.text(
                f'Failed request {md.bold("skiff.com")} with {res.status_code} status code{md.escape_md(".")} Reason:',
                md.code(res.text),
                sep = '\n\n'
            )

        content = res.json()
        logger.debug(content)
        if 'errors' in content[0]:
            error_message = content[0]['errors'][0]['message']
            logger.error(f'skiff.com returned error: {error_message}')
            return md.text(
                f'{md.bold("skiff.com")} returned error:',
                md.code(error_message),
                sep = '\n\n'
            )

        return content[0]['data']['mailbox']['threads']