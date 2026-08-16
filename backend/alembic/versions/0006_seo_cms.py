"""Table CMS blog_posts pour le SEO éditorial."""

from alembic import op

from app.database import Base
from app import models  # noqa: F401

revision = "0006_seo_cms"
down_revision = "0005_integration_hooks"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)


def downgrade() -> None:
    op.drop_table("blog_posts")
