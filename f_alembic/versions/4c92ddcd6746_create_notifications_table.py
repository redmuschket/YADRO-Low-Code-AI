"""create notifications table

Revision ID: 4c92ddcd6746
Revises: 
Create Date: 2026-05-14 18:36:14.349194

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSON

from core.enum.notification_status import NotificationStatus
from core.enum.notification_type import NotificationType

# revision identifiers, used by Alembic.
revision = '4c92ddcd6746'
down_revision = None
branch_labels = None
depends_on = None

notification_status_enum = sa.Enum(
    NotificationStatus,
    name='notification_status_enum',
    create_type=True
)
notification_type_enum = sa.Enum(
    NotificationType,
    name='notification_type_enum',
    create_type=True
)

def upgrade():
    notification_status_enum.create(op.get_bind(), checkfirst=True)
    notification_type_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        'notifications',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('type', sa.String(20), nullable=False),
        sa.Column('recipient', sa.String(512), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('subject', JSON(), nullable=True),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )


def downgrade():
    op.drop_table('notifications')

    notification_status_enum.drop(op.get_bind(), checkfirst=True)
    notification_type_enum.drop(op.get_bind(), checkfirst=True)