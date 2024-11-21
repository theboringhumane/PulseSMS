from enum import Enum


class XPathSelectors(str, Enum):
    REMEMBER_ME_SLIDER = "//mat-slide-toggle"
    REMEMBER_ME_SLIDER_BUTTON = "//button[contains(@class, 'checked') or contains(@class, 'unselected')]"
    QR_CODE = "//mw-qr-code"
    CONVERSATION_LIST = "//mws-conversations-list"
    CONTACT_INPUT = "//mw-contact-chips-input//input"
    CONTACT_SELECTOR_BTN = "//mw-contact-selector-button//button"
    TYPE_TEXTAREA = "//mws-autosize-textarea//textarea"
    SEND_MESSAGE_BTN = "//mw-message-send-button//button[@aria-label='Send SMS']"
    STATUS_MESSAGE = "//mws-message-wrapper"
