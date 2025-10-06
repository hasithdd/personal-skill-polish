"""CLI tool for offline skill tracking updates."""

import json
from pathlib import Path
from typing import Optional

import typer
import yaml
from rich.console import Console
from rich.table import Table
from sqlalchemy.orm import Session

from backend.app import crud, schemas
from backend.app.database import Base, SessionLocal, engine

app = typer.Typer(help="Personal Skill Polish CLI - Track your AI/ML learning journey")
console = Console()

# Create database tables
Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    """Get database session."""
    return SessionLocal()


@app.command()
def init(
    roadmap_file: Optional[Path] = typer.Option(
        None, "--file", "-f", help="Path to roadmap JSON/YAML file"
    )
) -> None:
    """Initialize the skill tracker with roadmap data."""
    if roadmap_file and roadmap_file.exists():
        with open(roadmap_file) as f:
            if roadmap_file.suffix in [".yaml", ".yml"]:
                data = yaml.safe_load(f)
            else:
                data = json.load(f)

        db = get_db()
        try:
            for phase_data in data.get("phases", []):
                phase_create = schemas.PhaseCreate(**phase_data)
                crud.create_phase(db, phase_create)
            console.print("[green]✓[/green] Roadmap initialized successfully!")
        except Exception as e:
            console.print(f"[red]✗[/red] Error initializing roadmap: {e}")
        finally:
            db.close()
    else:
        console.print("[yellow]![/yellow] No roadmap file provided. Starting with empty tracker.")


@app.command()
def list_phases() -> None:
    """List all learning phases."""
    db = get_db()
    try:
        phases = crud.get_phases(db)
        if not phases:
            console.print("[yellow]No phases found. Use 'init' to load roadmap.[/yellow]")
            return

        table = Table(title="Learning Phases")
        table.add_column("ID", style="cyan")
        table.add_column("Order", style="magenta")
        table.add_column("Title", style="green")
        table.add_column("Progress", style="yellow")
        table.add_column("XP", style="blue")

        for phase in phases:
            table.add_row(
                str(phase.id),
                str(phase.order),
                phase.title,
                f"{phase.progress:.1f}%",
                str(phase.xp),
            )

        console.print(table)
    finally:
        db.close()


@app.command()
def show_phase(phase_id: int) -> None:
    """Show details of a specific phase."""
    db = get_db()
    try:
        phase = crud.get_phase(db, phase_id)
        if not phase:
            console.print(f"[red]Phase {phase_id} not found.[/red]")
            return

        console.print(f"\n[bold cyan]Phase {phase.order}: {phase.title}[/bold cyan]")
        console.print(f"[yellow]Goal:[/yellow] {phase.goal}")
        console.print(f"[yellow]Progress:[/yellow] {phase.progress:.1f}%")
        console.print(f"[yellow]XP:[/yellow] {phase.xp}")
        if phase.notes:
            console.print(f"[yellow]Notes:[/yellow] {phase.notes}")

        if phase.topics:
            console.print(f"\n[bold]Topics ({len(phase.topics)}):[/bold]")
            for topic in phase.topics:
                console.print(f"  • {topic.name} ({topic.progress:.1f}%)")
    finally:
        db.close()


@app.command()
def update_progress(
    phase_id: int,
    progress: float = typer.Option(..., "--progress", "-p", help="Progress percentage (0-100)"),
    xp: Optional[int] = typer.Option(None, "--xp", "-x", help="XP points to add"),
) -> None:
    """Update progress for a phase."""
    db = get_db()
    try:
        update_data = schemas.PhaseUpdate(progress=progress)
        if xp is not None:
            phase = crud.get_phase(db, phase_id)
            if phase:
                update_data.xp = phase.xp + xp

        updated_phase = crud.update_phase(db, phase_id, update_data)
        if updated_phase:
            console.print(f"[green]✓[/green] Phase {phase_id} updated!")
            console.print(f"  Progress: {updated_phase.progress:.1f}%")
            console.print(f"  XP: {updated_phase.xp}")
        else:
            console.print(f"[red]Phase {phase_id} not found.[/red]")
    finally:
        db.close()


@app.command()
def add_note(
    phase_id: int,
    note: str = typer.Option(..., "--note", "-n", help="Note to add"),
) -> None:
    """Add a note to a phase."""
    db = get_db()
    try:
        phase = crud.get_phase(db, phase_id)
        if not phase:
            console.print(f"[red]Phase {phase_id} not found.[/red]")
            return

        existing_notes = phase.notes or ""
        new_notes = f"{existing_notes}\n{note}".strip()
        update_data = schemas.PhaseUpdate(notes=new_notes)
        crud.update_phase(db, phase_id, update_data)
        console.print(f"[green]✓[/green] Note added to phase {phase_id}!")
    finally:
        db.close()


@app.command()
def stats() -> None:
    """Show overall progress statistics."""
    db = get_db()
    try:
        stats = crud.get_progress_stats(db)
        console.print("\n[bold cyan]Progress Statistics[/bold cyan]")
        console.print(f"Total Phases: {stats.total_phases}")
        console.print(f"Completed Phases: {stats.completed_phases}")
        console.print(f"Overall Progress: {stats.total_progress:.1f}%")
        console.print(f"Total XP: {stats.total_xp}")
    finally:
        db.close()


@app.command()
def export(
    output_file: Path = typer.Option(..., "--output", "-o", help="Output file path"),
    format: str = typer.Option("json", "--format", "-f", help="Export format (json/yaml)"),
) -> None:
    """Export roadmap data to JSON or YAML."""
    db = get_db()
    try:
        phases = crud.get_phases(db)
        phases_data = []

        for phase in phases:
            phase_dict = {
                "title": phase.title,
                "goal": phase.goal,
                "progress": phase.progress,
                "notes": phase.notes,
                "order": phase.order,
                "xp": phase.xp,
                "topics": [],
            }

            for topic in phase.topics:
                topic_dict = {
                    "name": topic.name,
                    "progress": topic.progress,
                    "notes": topic.notes,
                    "xp": topic.xp,
                    "subtopics": [
                        {
                            "name": st.name,
                            "completed": st.completed,
                            "notes": st.notes,
                            "xp": st.xp,
                        }
                        for st in topic.subtopics
                    ],
                    "mastery_components": [
                        {
                            "name": mc.name,
                            "level": mc.level,
                            "notes": mc.notes,
                        }
                        for mc in topic.mastery_components
                    ],
                }
                phase_dict["topics"].append(topic_dict)

            phases_data.append(phase_dict)

        export_data = {"phases": phases_data}

        with open(output_file, "w") as f:
            if format.lower() in ["yaml", "yml"]:
                yaml.dump(export_data, f, default_flow_style=False, sort_keys=False)
            else:
                json.dump(export_data, f, indent=2)

        console.print(f"[green]✓[/green] Roadmap exported to {output_file}")
    except Exception as e:
        console.print(f"[red]✗[/red] Error exporting roadmap: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    app()
