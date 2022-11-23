package main

import (
	"context"
	"database/sql"
	"fmt"
	"os"

	"github.com/spf13/cobra"
	"github.com/uptrace/bun"
	"github.com/uptrace/bun/dialect/pgdialect"
	"github.com/uptrace/bun/driver/pgdriver"
	"github.com/uptrace/bun/extra/bundebug"
)

var Version = "0.0.0"

func New(ctx context.Context, flags Flags) *App {
	sqldb := sql.OpenDB(pgdriver.NewConnector(pgdriver.WithDSN(flags.ConnectionString)))
	db := bun.NewDB(sqldb, pgdialect.New())

	db.AddQueryHook(bundebug.NewQueryHook(
		bundebug.WithVerbose(true),
		bundebug.FromEnv("BUNDEBUG"),
	))

	return &App{
		Ctx:   ctx,
		Flags: flags,
		DB:    db,
	}
}

func (app *App) Close() {
	app.DB.Close()
}

func main() {
	flags := Flags{
		ConnectionString: "postgres://postgres:@localhost:5432/impala?sslmode=disable",
		Port:             8080,
	}

	cmd := &cobra.Command{
		Use:     "impala",
		Version: Version,
		Short:   "Impala is an inventory API for music collections",
		Long:    "An API for managing and exploring digital and physical music libraries.\n\nSee https://github.com/wuvt/impala for more information.",
	}

	cmd.PersistentFlags().StringVarP(&flags.ConnectionString, "database", "d", flags.ConnectionString, "Database to connect to")

	cmd.AddCommand(NewCmdDB(&flags))
	cmd.AddCommand(NewCmdServe(&flags))

	if err := cmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}

func NewCmdDB(flags *Flags) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "db",
		Short: "Database maintenence commands",
	}

	initCmd := &cobra.Command{
		Use:   "init",
		Short: "Prepare the database for migrations",
		RunE: func(cmd *cobra.Command, args []string) error {
			app := New(cmd.Context(), *flags)
			defer app.Close()

			return InitDB(app)
		},
	}

	migrateCmd := &cobra.Command{
		Use:   "migrate",
		Short: "Run all pending migrations",
		RunE: func(cmd *cobra.Command, args []string) error {
			app := New(cmd.Context(), *flags)
			defer app.Close()

			return MigrateDB(app)
		},
	}

	rollbackCmd := &cobra.Command{
		Use:   "rollback",
		Short: "Rollback the last migration group",
		RunE: func(cmd *cobra.Command, args []string) error {
			app := New(cmd.Context(), *flags)
			defer app.Close()

			return RollbackDB(app)
		},
	}

	lockCmd := &cobra.Command{
		Use:   "lock",
		Short: "Lock database migrations",
		RunE: func(cmd *cobra.Command, args []string) error {
			app := New(cmd.Context(), *flags)
			defer app.Close()

			return LockDB(app)
		},
	}

	unlockCmd := &cobra.Command{
		Use:   "unlock",
		Short: "Unlock database migrations",
		RunE: func(cmd *cobra.Command, args []string) error {
			app := New(cmd.Context(), *flags)
			defer app.Close()

			return UnlockDB(app)
		},
	}

	statusCmd := &cobra.Command{
		Use:   "status",
		Short: "Display the current migration status",
		RunE: func(cmd *cobra.Command, args []string) error {
			app := New(cmd.Context(), *flags)
			defer app.Close()

			return StatusDB(app)
		},
	}

	markAppliedCmd := &cobra.Command{
		Use:   "mark",
		Short: "Mark migrations as applied without running them",
		RunE: func(cmd *cobra.Command, args []string) error {
			app := New(cmd.Context(), *flags)
			defer app.Close()

			return MarkAppliedDB(app)
		},
	}

	unmarkAppliedCmd := &cobra.Command{
		Use:   "unmark",
		Short: "Unmark the last migration group without rolling back",
		RunE: func(cmd *cobra.Command, args []string) error {
			app := New(cmd.Context(), *flags)
			defer app.Close()

			return UnmarkAppliedDB(app)
		},
	}

	cmd.AddCommand(initCmd)
	cmd.AddCommand(migrateCmd)
	cmd.AddCommand(rollbackCmd)
	cmd.AddCommand(lockCmd)
	cmd.AddCommand(unlockCmd)
	cmd.AddCommand(statusCmd)
	cmd.AddCommand(markAppliedCmd)
	cmd.AddCommand(unmarkAppliedCmd)

	return cmd
}

func NewCmdServe(flags *Flags) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "serve",
		Short: "Start the Impala metadata server",
		Run: func(cmd *cobra.Command, args []string) {
			fmt.Println("TODO: Serve on port", flags.Port)
		},
	}

	cmd.Flags().Uint16VarP(&flags.Port, "port", "p", flags.Port, "Port to run on")

	return cmd
}
