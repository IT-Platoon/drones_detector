"""empty message

Revision ID: e2b6fd50c753
Revises: 
Create Date: 2024-04-19 08:08:46.129500

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'e2b6fd50c753'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('detection_task',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('status', sa.Enum('CREATED', 'FINISHED', name='detectiontaskstatus'), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__detection_task')),
    sa.UniqueConstraint('id', name=op.f('uq__detection_task__id'))
    )
    op.create_table('detection_item',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('origin_file', sa.TEXT(), nullable=False),
    sa.Column('type', sa.Enum('IMAGE', 'VIDEO', name='detectionitemtype'), nullable=False),
    sa.Column('predict_file', sa.TEXT(), nullable=True),
    sa.Column('classes', sa.TEXT(), nullable=True),
    sa.Column('detection_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['detection_id'], ['detection_task.id'], name=op.f('fk__detection_item__detection_id__detection_task')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__detection_item')),
    sa.UniqueConstraint('id', name=op.f('uq__detection_item__id'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('detection_item')
    op.drop_table('detection_task')
    # ### end Alembic commands ###