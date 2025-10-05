HELP_NS = "help"

def k(*parts):
    return ":".join((HELP_NS,) + parts)

def user_key(uid): return k("user", uid)
def agent_key(aid): return k("agent", aid)
def agent_skills(aid): return k("agent", aid, "skills")
def agent_open(aid): return k("agent", aid, "open_tickets")
def ticket_key(tid): return k("ticket", tid)
def ticket_log(tid): return k("ticket", tid, "log")

IDX_USER_EMAIL = k("idx","user_email")
def user_email_key(email): return f"{IDX_USER_EMAIL}:{email}"
PRIORITY_Q = k("queue","priority")

ALL_TICKETS = k("tickets")
SEQ_USERS = k("seq","users")
SEQ_AGENTS = k("seq","agents")
SEQ_TICKETS = k("seq","tickets")

STATUSES = ("open","in_progress","on_hold","closed")

def as_member_ticket(tid): return f"ticket:{tid}"
