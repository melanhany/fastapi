"""new migration

Revision ID: 5a19254b6f70
Revises: b6a61bb29d52
Create Date: 2023-09-05 21:54:10.497948

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a19254b6f70'
down_revision: Union[str, None] = 'b6a61bb29d52'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
