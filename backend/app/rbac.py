from app.models.enums import UserRole

STAFF = {UserRole.RECRUITER, UserRole.ADMIN, UserRole.FINANCE, UserRole.EDITOR}
INTERNAL = {UserRole.RECRUITER, UserRole.ADMIN}
ADMINS = {UserRole.ADMIN}

PERMISSIONS: dict[str, set[UserRole]] = {
    "jobs:read_public": set(UserRole),
    "jobs:manage": {UserRole.EMPLOYER, UserRole.RECRUITER, UserRole.ADMIN},
    "jobs:publish": {UserRole.EMPLOYER, UserRole.RECRUITER, UserRole.ADMIN},
    "applications:create": {UserRole.CANDIDATE},
    "applications:own_read": {UserRole.CANDIDATE},
    "applications:manage": {UserRole.EMPLOYER, UserRole.RECRUITER, UserRole.ADMIN},
    "candidates:self": {UserRole.CANDIDATE},
    "candidates:manage": {UserRole.RECRUITER, UserRole.ADMIN},
    "companies:self": {UserRole.EMPLOYER},
    "companies:manage": {UserRole.RECRUITER, UserRole.ADMIN},
    "notes:write": {UserRole.RECRUITER, UserRole.ADMIN},
    "missions:manage": {UserRole.RECRUITER, UserRole.ADMIN},
    "admin:all": {UserRole.ADMIN},
    "finance:read": {UserRole.ADMIN, UserRole.FINANCE},
    "content:manage": {UserRole.ADMIN, UserRole.EDITOR},
    "notifications:self": set(UserRole),
}


def can(role: UserRole, permission: str) -> bool:
    if role == UserRole.ADMIN:
        return True
    allowed = PERMISSIONS.get(permission)
    return bool(allowed and role in allowed)
