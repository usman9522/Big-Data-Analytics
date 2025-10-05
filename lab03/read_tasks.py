from helpdesk_conn import get_redis
from models import *
from collections import Counter

r = get_redis()

def resolve_user_by_email(email):
    uid = r.get(user_email_key(email))
    return uid, r.hgetall(user_key(uid)) if uid else None

def top_priority(n=3):
    return r.zrevrange(PRIORITY_Q, 0, n-1, withscores=True)

def agent_open_ticket_subjects(aid):
    members = r.smembers(agent_open(aid))
    out = []
    for m in members:
        tid = m.split(":")[1]
        out.append((tid, r.hget(ticket_key(tid), "subject")))
    return out

def ticket_timeline(tid):
    return r.lrange(ticket_log(tid), 0, -1)

def count_by_status():
    counts = Counter()
    for tid in r.smembers(ALL_TICKETS):
        st = r.hget(ticket_key(tid), "status")
        counts[st] += 1
    return dict(counts)

def agents_with_skill(skill):
    ids = []
    for key in r.scan_iter(agent_skills("*")):
        aid = key.split(":")[2]
        if r.sismember(agent_skills(aid), skill):
            ids.append(aid)
    return ids

if __name__ == "__main__":
    print("Resolve user by email:", resolve_user_by_email("aisha@example.com"))
    print("Top-3 priority tickets:", top_priority(3))
    print("Agent 1 open tickets:", agent_open_ticket_subjects("1"))
    print("Ticket 1 timeline:", ticket_timeline("1"))
    print("Counts by status:", count_by_status())
    print("Agents covering 'returns':", agents_with_skill("returns"))
