import os
import psycopg2

from scripts import (
        nofluffjobs,
        justjoinit
    )

def main():
    nofluffjobs.NoFluffJobs().get_jobs_from_api()
    justjoinit.JustJoinIT().get_jobs_from_api()
    print("finito?!")

if __name__ == "__main__":
    main()