from helpdesk_conn import get_redis
from models import *

r = get_redis()

def business_close(tid):
    r.hset(ticket_key(tid), mapping={"status": "closed"})
    r.zrem(PRIORITY_Q, as_member_ticket(tid))
    aid = r.hget(ticket_key(tid), "assigned_agent")
    if aid:
        r.srem(agent_open(aid), as_member_ticket(tid))
        r.hincrby(agent_key(aid), "load", -1)
    r.rpush(ticket_log(tid), "closed")

def hard_delete_ticket(tid):
    r.zrem(PRIORITY_Q, as_member_ticket(tid))
    r.delete(ticket_log(tid))
    r.srem(ALL_TICKETS, tid)
    aid = r.hget(ticket_key(tid), "assigned_agent")
    if aid:
        r.srem(agent_open(aid), as_member_ticket(tid))
        r.hincrby(agent_key(aid), "load", -1)
    r.delete(ticket_key(tid))

def delete_user(uid):
    email = r.hget(user_key(uid), "email")
    if email:
        r.delete(user_email_key(email))
    r.delete(user_key(uid))

def cleanup_lab_keys():
    to_del = list(r.scan_iter("help:*"))
    for k in to_del:
        r.delete(k)
    return to_del

if __name__ == "__main__":
    business_close("3")
    hard_delete_ticket("4")
    delete_user("1")
    # deleted = cleanup_lab_keys()
    # print("Deleted keys:", deleted)
    print("Delete tasks done.")
