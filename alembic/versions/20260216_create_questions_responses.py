"""create questions and responses tables

Revision ID: create_questions_responses
Revises: 
Create Date: 2026-02-16 09:00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = 'create_questions_responses'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'questions',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('text', sa.String, nullable=False),
    )

    op.create_table(
        'responses',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('question_id', sa.Integer, sa.ForeignKey('questions.id')),
        sa.Column('answer', sa.String, nullable=False),
    )


def downgrade():
    op.drop_table('responses')
    op.drop_table('questions')