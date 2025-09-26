from aiogram.types import update

from src.database.db_session import db_session
from src.database.models import ConsoleCommand
from sqlalchemy import select, delete, update

async def select_one_command(name: str) -> ConsoleCommand:
    async with db_session() as session:
        command = await session.execute(select(ConsoleCommand).where(ConsoleCommand.name == name))
        return command.scalar_one_or_none()

async def select_commands() -> list[ConsoleCommand]:
    async with db_session() as session:
        commands = await session.execute(select(ConsoleCommand))
        return commands.scalars().all()

async def insert_command(name: str, description: str, result: str) -> None:
    async with db_session() as session:
        command = ConsoleCommand(name=name, description=description, result=result)

        session.add(command)
        await session.commit()

async def update_command(name: str, n_description: str, n_result: str) -> None:
    async with db_session() as session:
        statement = (update(ConsoleCommand)
                     .where(ConsoleCommand.name == name)
                     .values(description=n_description, result=n_result)
                     )

        await session.execute(statement)
        await session.commit()


async def delete_command(name: str) -> None:
    async with db_session() as session:

        await session.execute(delete(ConsoleCommand).where(ConsoleCommand.name == name))
        await session.commit()



