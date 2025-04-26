from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `things` ADD `is_finish` BOOL NOT NULL DEFAULT 0;
        ALTER TABLE `things` ADD `create_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `things` DROP COLUMN `is_finish`;
        ALTER TABLE `things` DROP COLUMN `create_at`;"""
