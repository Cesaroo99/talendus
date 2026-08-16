from app.models.enums import CompanyMemberRole, UserRole

ADMINS = {UserRole.ADMIN, UserRole.SUPER_ADMIN}
STAFF = {UserRole.RECRUITER, UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.FINANCE, UserRole.EDITOR}
INTERNAL = {UserRole.RECRUITER, UserRole.ADMIN, UserRole.SUPER_ADMIN}


def is_admin(user_or_role) -> bool:
    role = getattr(user_or_role, "role", user_or_role)
    return role in ADMINS

PERMISSIONS: dict[str, set[UserRole]] = {
    "jobs:read_public": set(UserRole),
    "jobs:manage": {UserRole.EMPLOYER, UserRole.RECRUITER, UserRole.ADMIN, UserRole.SUPER_ADMIN},
    "jobs:publish": {UserRole.EMPLOYER, UserRole.RECRUITER, UserRole.ADMIN, UserRole.SUPER_ADMIN},
    "applications:create": {UserRole.CANDIDATE},
    "applications:own_read": {UserRole.CANDIDATE},
    "applications:manage": {UserRole.RECRUITER, UserRole.ADMIN, UserRole.SUPER_ADMIN},
    "applications:presented": {UserRole.EMPLOYER, UserRole.RECRUITER, UserRole.ADMIN, UserRole.SUPER_ADMIN},
    "candidates:self": {UserRole.CANDIDATE},
    "candidates:manage": {UserRole.RECRUITER, UserRole.ADMIN, UserRole.SUPER_ADMIN},
    "companies:self": {UserRole.EMPLOYER},
    "companies:manage": {UserRole.RECRUITER, UserRole.ADMIN, UserRole.SUPER_ADMIN},
    "notes:write": {UserRole.RECRUITER, UserRole.ADMIN, UserRole.SUPER_ADMIN},
    "missions:manage": {UserRole.RECRUITER, UserRole.ADMIN, UserRole.SUPER_ADMIN},
    "admin:all": {UserRole.ADMIN, UserRole.SUPER_ADMIN},
    "finance:read": {UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.FINANCE},
    "content:manage": {UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.EDITOR},
    "notifications:self": set(UserRole),
    "messages:use": set(UserRole),
    "interviews:manage": {UserRole.RECRUITER, UserRole.ADMIN, UserRole.SUPER_ADMIN},
    "interviews:own": {UserRole.CANDIDATE, UserRole.EMPLOYER, UserRole.RECRUITER, UserRole.ADMIN, UserRole.SUPER_ADMIN},
    "interviews:create": {UserRole.RECRUITER, UserRole.ADMIN, UserRole.SUPER_ADMIN},
    "documents:self": {UserRole.CANDIDATE, UserRole.EMPLOYER, UserRole.RECRUITER, UserRole.ADMIN, UserRole.SUPER_ADMIN},
    "jobs:save": {UserRole.CANDIDATE},
    "company:members": {UserRole.EMPLOYER, UserRole.ADMIN, UserRole.SUPER_ADMIN},
    "invoices:manage": {UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.FINANCE},
    "invoices:read": {UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.FINANCE, UserRole.EMPLOYER, UserRole.RECRUITER},
    "contracts:sign": {UserRole.EMPLOYER, UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.RECRUITER},
    "matching:read": {UserRole.CANDIDATE, UserRole.RECRUITER, UserRole.ADMIN, UserRole.SUPER_ADMIN},
    "settings:manage": {UserRole.ADMIN, UserRole.SUPER_ADMIN},
}


def can(role: UserRole, permission: str) -> bool:
    if is_admin(role):
        return True
    allowed = PERMISSIONS.get(permission)
    return bool(allowed and role in allowed)


COMPANY_PERMISSIONS: dict[str, set[CompanyMemberRole]] = {
    "company:write": {CompanyMemberRole.OWNER, CompanyMemberRole.ADMIN},
    "members:manage": {CompanyMemberRole.OWNER, CompanyMemberRole.ADMIN},
    "jobs:write": {CompanyMemberRole.OWNER, CompanyMemberRole.ADMIN, CompanyMemberRole.HR, CompanyMemberRole.RECRUITER},
    "applications:write": {
        CompanyMemberRole.OWNER,
        CompanyMemberRole.ADMIN,
        CompanyMemberRole.HR,
        CompanyMemberRole.RECRUITER,
    },
    "interviews:write": {
        CompanyMemberRole.OWNER,
        CompanyMemberRole.ADMIN,
        CompanyMemberRole.HR,
        CompanyMemberRole.RECRUITER,
    },
    "invoices:read": {CompanyMemberRole.OWNER, CompanyMemberRole.ADMIN, CompanyMemberRole.BILLING},
    "documents:write": {CompanyMemberRole.OWNER, CompanyMemberRole.ADMIN, CompanyMemberRole.HR},
    "company:read": set(CompanyMemberRole),
}


def company_can(member_role: CompanyMemberRole | None, permission: str) -> bool:
    if member_role is None:
        return False
    if member_role in {CompanyMemberRole.OWNER, CompanyMemberRole.ADMIN}:
        return True
    allowed = COMPANY_PERMISSIONS.get(permission)
    return bool(allowed and member_role in allowed)
