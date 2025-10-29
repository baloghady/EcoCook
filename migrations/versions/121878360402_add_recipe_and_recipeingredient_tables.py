"""add recipe and recipeingredient tables

Revision ID: 121878360402
Revises: c3a1218ddac9
Create Date: 2025-10-27 00:23:17.505283

"""
from alembic import op
import sqlalchemy as sa


revision = '121878360402'
down_revision = 'c3a1218ddac9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('recipe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('servings', sa.Integer(), nullable=True),
    sa.Column('prep_time', sa.Integer(), nullable=True),
    sa.Column('cook_time', sa.Integer(), nullable=True),
    sa.Column('difficulty', sa.String(length=20), nullable=True),
    sa.Column('cuisine', sa.String(length=50), nullable=True),
    sa.Column('dietary_tags', sa.JSON(), nullable=True),
    sa.Column('instructions', sa.JSON(), nullable=True),
    sa.Column('nutrition', sa.JSON(), nullable=True),
    sa.Column('image_url', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('rating_sum', sa.Integer(), nullable=True),
    sa.Column('rating_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recipe_ingredient',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('ingredient_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.Column('unit', sa.String(length=20), nullable=False),
    sa.Column('is_optional', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['ingredient_id'], ['ingredient.id'], ),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('cooking_history', schema=None) as batch_op:
        batch_op.add_column(sa.Column('recipe_id', sa.Integer(), nullable=True))
        batch_op.alter_column('ingredient_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.create_foreign_key('fk_cooking_history_recipe_id', 'recipe', ['recipe_id'], ['id'])


def downgrade():
    with op.batch_alter_table('cooking_history', schema=None) as batch_op:
        batch_op.drop_constraint('fk_cooking_history_recipe_id', type_='foreignkey')
        batch_op.alter_column('ingredient_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_column('recipe_id')

    op.drop_table('recipe_ingredient')
    op.drop_table('recipe')
