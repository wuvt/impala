package main

import (
	"fmt"

	"github.com/wuvt/impala/migrations"

	"github.com/uptrace/bun/migrate"
)

func InitDB(app *App) error {
	migrator := migrate.NewMigrator(app.DB, migrations.Migrations)
	return migrator.Init(app.Ctx)
}

func MigrateDB(app *App) error {
	migrator := migrate.NewMigrator(app.DB, migrations.Migrations)

	group, err := migrator.Migrate(app.Ctx)
	if err != nil {
		return err
	}

	if group.ID == 0 {
		fmt.Println("No new migrations to run.")
		return nil
	}

	fmt.Println("Migrated to", group)
	return nil
}

func RollbackDB(app *App) error {
	migrator := migrate.NewMigrator(app.DB, migrations.Migrations)

	group, err := migrator.Rollback(app.Ctx)
	if err != nil {
		return err
	}

	if group.ID == 0 {
		fmt.Println("There are no migrations to roll back.")
		return nil
	}

	fmt.Println("Rolled back", group)
	return nil
}

func LockDB(app *App) error {
	migrator := migrate.NewMigrator(app.DB, migrations.Migrations)
	return migrator.Lock(app.Ctx)
}

func UnlockDB(app *App) error {
	migrator := migrate.NewMigrator(app.DB, migrations.Migrations)
	return migrator.Unlock(app.Ctx)
}

func StatusDB(app *App) error {
	migrator := migrate.NewMigrator(app.DB, migrations.Migrations)

	ms, err := migrator.MigrationsWithStatus(app.Ctx)
	if err != nil {
		return err
	}

	fmt.Println("Migrations:", ms)
	fmt.Println("Unapplied migrations:", ms.Unapplied())
	fmt.Println("Last migration group:", ms.LastGroup())
	return nil
}

func MarkAppliedDB(app *App) error {
	migrator := migrate.NewMigrator(app.DB, migrations.Migrations)

	group, err := migrator.Migrate(app.Ctx, migrate.WithNopMigration())
	if err != nil {
		return err
	}

	if group.ID == 0 {
		fmt.Println("No new migrations to mark.")
		return nil
	}

	fmt.Println("Marked", group)
	return nil
}

func UnmarkAppliedDB(app *App) error {
	migrator := migrate.NewMigrator(app.DB, migrations.Migrations)

	group, err := migrator.Rollback(app.Ctx, migrate.WithNopMigration())
	if err != nil {
		return err
	}

	if group.ID == 0 {
		fmt.Println("There are no migrations to unmark.")
		return nil
	}

	fmt.Println("Unmarked", group)
	return nil
}
