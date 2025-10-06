"""
CLI tool for Personal Skill Tracker using Typer
"""
import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress as RichProgress, BarColumn, TextColumn
from rich.panel import Panel
from rich import box
from typing import Optional
import json
from datetime import datetime
from sqlalchemy.orm import Session

from backend.app.db import SessionLocal
from backend.app.models import Phase, Topic, Subtopic, Progress, Note, Stats, Achievement

app = typer.Typer(help="Personal Skill Tracker CLI - Track your AI/ML learning journey")
console = Console()


def get_db() -> Session:
    """Get database session"""
    return SessionLocal()


@app.command()
def list_phases():
    """List all learning phases"""
    db = get_db()
    try:
        phases = db.query(Phase).order_by(Phase.order).all()

        table = Table(title="AI/ML Learning Phases", box=box.ROUNDED)
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Phase", style="magenta")
        table.add_column("Description", style="white")
        table.add_column("Topics", justify="center", style="green")

        for phase in phases:
            table.add_row(
                str(phase.id),
                phase.name,
                phase.description[:50] + "..."
                if len(phase.description or "") > 50
                else phase.description or "",
                str(len(phase.topics)),
            )

        console.print(table)
    finally:
        db.close()


@app.command()
def list_topics(phase_id: Optional[int] = typer.Option(None, help="Filter by phase ID")):
    """List all topics, optionally filtered by phase"""
    db = get_db()
    try:
        query = db.query(Topic).join(Phase)
        if phase_id:
            query = query.filter(Topic.phase_id == phase_id)
        topics = query.order_by(Phase.order, Topic.order).all()

        table = Table(
            title=f"Topics{' for Phase ' + str(phase_id) if phase_id else ''}", box=box.ROUNDED
        )
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Phase", style="yellow")
        table.add_column("Topic", style="magenta")
        table.add_column("Subtopics", justify="center", style="green")

        for topic in topics:
            table.add_row(str(topic.id), topic.phase.name, topic.name, str(len(topic.subtopics)))

        console.print(table)
    finally:
        db.close()


@app.command()
def list_subtopics(topic_id: Optional[int] = typer.Option(None, help="Filter by topic ID")):
    """List all subtopics, optionally filtered by topic"""
    db = get_db()
    try:
        query = db.query(Subtopic).join(Topic).join(Phase)
        if topic_id:
            query = query.filter(Subtopic.topic_id == topic_id)
        subtopics = query.order_by(Phase.order, Topic.order, Subtopic.order).all()

        table = Table(
            title=f"Subtopics{' for Topic ' + str(topic_id) if topic_id else ''}", box=box.ROUNDED
        )
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Topic", style="yellow")
        table.add_column("Subtopic", style="magenta")
        table.add_column("Components", justify="center", style="green")

        for subtopic in subtopics:
            table.add_row(
                str(subtopic.id),
                subtopic.topic.name,
                subtopic.name,
                str(len(subtopic.mastery_components)),
            )

        console.print(table)
    finally:
        db.close()


@app.command()
def update_progress(
    subtopic_id: int = typer.Argument(..., help="Subtopic ID to update"),
    status: str = typer.Option("in_progress", help="Status: not_started, in_progress, completed"),
    percentage: float = typer.Option(None, help="Completion percentage (0-100)"),
    hours: float = typer.Option(None, help="Hours spent"),
):
    """Update progress for a subtopic"""
    db = get_db()
    try:
        subtopic = db.query(Subtopic).filter(Subtopic.id == subtopic_id).first()
        if not subtopic:
            console.print(f"[red]Subtopic with ID {subtopic_id} not found[/red]")
            return

        # Find or create progress record
        progress = db.query(Progress).filter(Progress.subtopic_id == subtopic_id).first()
        if not progress:
            progress = Progress(subtopic_id=subtopic_id)
            db.add(progress)

        # Update fields
        progress.status = status
        progress.last_studied = datetime.utcnow()

        if percentage is not None:
            progress.completion_percentage = min(max(percentage, 0), 100)

        if hours is not None:
            progress.hours_spent = hours

        db.commit()

        console.print(
            Panel(
                f"[green]✓[/green] Updated progress for: {subtopic.name}\n"
                f"Status: {progress.status}\n"
                f"Completion: {progress.completion_percentage}%\n"
                f"Hours: {progress.hours_spent}",
                title="Progress Updated",
                border_style="green",
            )
        )
    except Exception as e:
        console.print(f"[red]Error updating progress: {e}[/red]")
        db.rollback()
    finally:
        db.close()


@app.command()
def add_note(
    subtopic_id: int = typer.Argument(..., help="Subtopic ID"),
    content: str = typer.Argument(..., help="Note content"),
):
    """Add a note to a subtopic's progress"""
    db = get_db()
    try:
        # Find or create progress record
        progress = db.query(Progress).filter(Progress.subtopic_id == subtopic_id).first()
        if not progress:
            progress = Progress(subtopic_id=subtopic_id)
            db.add(progress)
            db.flush()

        note = Note(progress_id=progress.id, content=content)
        db.add(note)
        db.commit()

        console.print(f"[green]✓ Note added successfully[/green]")
    except Exception as e:
        console.print(f"[red]Error adding note: {e}[/red]")
        db.rollback()
    finally:
        db.close()


@app.command()
def dashboard():
    """Show overall dashboard with stats and progress"""
    db = get_db()
    try:
        stats = db.query(Stats).first()
        if not stats:
            stats = Stats()
            db.add(stats)
            db.commit()

        # Create stats panel
        stats_text = (
            f"[cyan]Total Points:[/cyan] {stats.total_points}\n"
            f"[cyan]Total Hours:[/cyan] {stats.total_hours}\n"
            f"[cyan]Current Streak:[/cyan] {stats.current_streak} days\n"
            f"[cyan]Longest Streak:[/cyan] {stats.longest_streak} days\n"
            f"[cyan]Phases Completed:[/cyan] {stats.phases_completed}\n"
            f"[cyan]Topics Completed:[/cyan] {stats.topics_completed}\n"
            f"[cyan]Subtopics Completed:[/cyan] {stats.subtopics_completed}"
        )
        console.print(Panel(stats_text, title="📊 Overall Stats", border_style="cyan"))

        # Show phase progress
        phases = db.query(Phase).order_by(Phase.order).all()

        console.print("\n[bold]Phase Progress:[/bold]")
        for phase in phases:
            total_subtopics = sum(len(topic.subtopics) for topic in phase.topics)
            completed_subtopics = sum(
                1
                for topic in phase.topics
                for subtopic in topic.subtopics
                if any(p.status == "completed" for p in subtopic.progress)
            )

            percentage = (completed_subtopics / total_subtopics * 100) if total_subtopics > 0 else 0

            with RichProgress() as progress:
                task = progress.add_task(f"[cyan]{phase.name}", total=100)
                progress.update(task, completed=percentage)

            console.print(f"  {completed_subtopics}/{total_subtopics} subtopics completed")

        # Show achievements
        achievements = db.query(Achievement).filter(Achievement.unlocked == True).all()
        if achievements:
            console.print("\n[bold]🏆 Achievements Unlocked:[/bold]")
            for achievement in achievements:
                console.print(
                    f"  {achievement.icon} {achievement.name} - {achievement.points} points"
                )

    finally:
        db.close()


@app.command()
def export(output_file: str = typer.Option("skill_tracker_export.json", help="Output JSON file")):
    """Export all data to JSON"""
    db = get_db()
    try:
        data = {"exported_at": datetime.utcnow().isoformat(), "phases": []}

        phases = db.query(Phase).order_by(Phase.order).all()
        for phase in phases:
            phase_data = {
                "id": phase.id,
                "name": phase.name,
                "description": phase.description,
                "order": phase.order,
                "topics": [],
            }

            for topic in phase.topics:
                topic_data = {
                    "id": topic.id,
                    "name": topic.name,
                    "description": topic.description,
                    "order": topic.order,
                    "subtopics": [],
                }

                for subtopic in topic.subtopics:
                    progress = (
                        db.query(Progress).filter(Progress.subtopic_id == subtopic.id).first()
                    )
                    subtopic_data = {
                        "id": subtopic.id,
                        "name": subtopic.name,
                        "description": subtopic.description,
                        "order": subtopic.order,
                        "progress": {
                            "status": progress.status if progress else "not_started",
                            "completion_percentage": progress.completion_percentage
                            if progress
                            else 0,
                            "hours_spent": progress.hours_spent if progress else 0,
                        },
                    }
                    topic_data["subtopics"].append(subtopic_data)

                phase_data["topics"].append(topic_data)

            data["phases"].append(phase_data)

        with open(output_file, "w") as f:
            json.dump(data, f, indent=2)

        console.print(f"[green]✓ Data exported to {output_file}[/green]")
    except Exception as e:
        console.print(f"[red]Error exporting data: {e}[/red]")
    finally:
        db.close()


@app.command()
def stats():
    """Show detailed statistics"""
    db = get_db()
    try:
        stats_obj = db.query(Stats).first()
        if not stats_obj:
            console.print("[yellow]No statistics available yet[/yellow]")
            return

        table = Table(title="📊 Statistics", box=box.DOUBLE)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Total Points", str(stats_obj.total_points))
        table.add_row("Total Hours", f"{stats_obj.total_hours:.1f}")
        table.add_row("Current Streak", f"{stats_obj.current_streak} days")
        table.add_row("Longest Streak", f"{stats_obj.longest_streak} days")
        table.add_row("Phases Completed", str(stats_obj.phases_completed))
        table.add_row("Topics Completed", str(stats_obj.topics_completed))
        table.add_row("Subtopics Completed", str(stats_obj.subtopics_completed))

        console.print(table)
    finally:
        db.close()


@app.command()
def achievements():
    """Show all achievements"""
    db = get_db()
    try:
        all_achievements = db.query(Achievement).all()

        table = Table(title="🏆 Achievements", box=box.ROUNDED)
        table.add_column("Icon", style="yellow")
        table.add_column("Name", style="magenta")
        table.add_column("Description", style="white")
        table.add_column("Points", justify="center", style="green")
        table.add_column("Status", justify="center", style="cyan")

        for achievement in all_achievements:
            status = "✓ Unlocked" if achievement.unlocked else "Locked"
            style = "green" if achievement.unlocked else "dim"
            table.add_row(
                achievement.icon or "🎯",
                achievement.name,
                achievement.description or "",
                str(achievement.points),
                status,
                style=style,
            )

        console.print(table)
    finally:
        db.close()


if __name__ == "__main__":
    app()
