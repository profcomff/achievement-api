"""init

Revision ID: c06c1cd9939c
Revises:
Create Date: 2023-08-18 03:21:29.803878

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c06c1cd9939c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'achievement',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('picture', sa.String(), nullable=False),
        sa.Column('owner_user_id', sa.Integer(), nullable=False),
        sa.Column('create_ts', sa.DateTime(), nullable=False),
        sa.Column('update_ts', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'achievement_reciever',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('achievement_id', sa.Integer(), nullable=False),
        sa.Column('create_ts', sa.DateTime(), nullable=False),
        sa.Column('update_ts', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ['achievement_id'],
            ['achievement.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('achievement_reciever')
    op.drop_table('achievement')
