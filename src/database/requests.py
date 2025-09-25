from src.database.db_session import db_session
from src.database.models import ConsoleCommand
from sqlalchemy import select

async def select_commands() -> list[ConsoleCommand]:
    async with db_session() as session:
        results = await session.execute(select(ConsoleCommand))
        commands = results.scalars().all()
        return commands

async def insert_command(name: str, description: str, result: str) -> None:
    async with db_session() as session:
        command = ConsoleCommand(name=name, description=description, result=result)

        session.add(command)
        await session.commit()



