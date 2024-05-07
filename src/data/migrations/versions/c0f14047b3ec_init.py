"""init

Revision ID: c0f14047b3ec
Revises: 2af689623d77
Create Date: 2024-05-06 19:02:23.159639

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0f14047b3ec'
down_revision: Union[str, None] = '2af689623d77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('letters', sa.Column('answer', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('letters', 'answer')
    # ### end Alembic commands ###