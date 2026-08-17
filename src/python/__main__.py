import argparse
import sys
from scheduler.csv_parser import CSVParser
from scheduler.scheduler import DegreeScheduler


def main():
    """Main entry point for the Degree Planner CLI."""
    parser = argparse.ArgumentParser(
        description='Generate personalized 4-year degree plans',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m scheduler --input data/courses.csv --output schedule.txt
  python -m scheduler --input data/courses.csv --output schedule.txt --credits 16
        """
    )

    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Path to CSV file with course data'
    )
    parser.add_argument(
        '--output', '-o',
        default='schedule.txt',
        help='Output file path (default: schedule.txt)'
    )
    parser.add_argument(
        '--credits', '-c',
        type=float,
        default=15.0,
        help='Target credits per semester (default: 15.0)'
    )
    parser.add_argument(
        '--semesters', '-s',
        type=int,
        default=8,
        help='Number of semesters (default: 8 for 4 years)'
    )

    args = parser.parse_args()

    try:
        print("Parsing course data...")
        courses = CSVParser.parse_courses(args.input)
        print(f"Loaded {len(courses)} courses")

        print("Building prerequisite graph...")
        scheduler = DegreeScheduler(courses)

        print("Generating optimal schedule...")
        schedule = scheduler.schedule(
            target_credits_per_semester=args.credits,
            num_semesters=args.semesters
        )

        print("Creating schedule summary...")
        summary = scheduler.get_schedule_summary(schedule)

        # Write to file
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(summary)

        print(f"\nSuccess! Schedule saved to: {args.output}")
        print(summary)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
