"""empty message

Revision ID: f033e360a3d7
Revises: 
Create Date: 2019-07-15 14:31:39.149119

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f033e360a3d7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('weight', sa.Integer(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('member',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nickname', sa.String(length=100), nullable=False),
    sa.Column('mobile', sa.String(length=11), nullable=False),
    sa.Column('gender', sa.Integer(), nullable=False),
    sa.Column('avatar', sa.String(length=200), nullable=False),
    sa.Column('salt', sa.String(length=32), nullable=False),
    sa.Column('reg_ip', sa.String(length=100), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('role', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('head_img', sa.String(length=1024), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('food',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('main_image', sa.String(length=100), nullable=False),
    sa.Column('summary', sa.String(length=2000), nullable=False),
    sa.Column('stock', sa.Integer(), nullable=False),
    sa.Column('tags', sa.String(length=200), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('month_count', sa.Integer(), nullable=False),
    sa.Column('total_count', sa.Integer(), nullable=False),
    sa.Column('view_count', sa.Integer(), nullable=False),
    sa.Column('comment_count', sa.Integer(), nullable=False),
    sa.Column('cat_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cat_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('member_address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.Column('nickname', sa.String(length=20), nullable=False),
    sa.Column('mobile', sa.String(length=11), nullable=False),
    sa.Column('province_id', sa.Integer(), nullable=False),
    sa.Column('province_str', sa.String(length=50), nullable=False),
    sa.Column('city_id', sa.Integer(), nullable=False),
    sa.Column('city_str', sa.String(length=50), nullable=False),
    sa.Column('area_id', sa.Integer(), nullable=False),
    sa.Column('area_str', sa.String(length=50), nullable=False),
    sa.Column('address', sa.String(length=100), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('is_default', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['member_id'], ['member.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('oauth_member_bind',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client_type', sa.String(length=20), nullable=False),
    sa.Column('type', sa.Integer(), nullable=False),
    sa.Column('openid', sa.String(length=80), nullable=False),
    sa.Column('unionid', sa.String(length=100), nullable=False),
    sa.Column('extra', sa.Text(), nullable=False),
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['member_id'], ['member.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('member_cart',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.Column('food_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['food_id'], ['food.id'], ),
    sa.ForeignKeyConstraint(['member_id'], ['member.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('member_cart')
    op.drop_table('oauth_member_bind')
    op.drop_table('member_address')
    op.drop_table('food')
    op.drop_table('user')
    op.drop_table('member')
    op.drop_table('category')
    # ### end Alembic commands ###
