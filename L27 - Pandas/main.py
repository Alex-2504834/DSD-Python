from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable, Dict, FrozenSet, List, Mapping, Optional, Sequence, Tuple

import kagglehub
import matplotlib.pyplot as plot
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure


class CsvTable(Enum):
    circuits = "circuits.csv"
    constructorResults = "constructor_results.csv"
    constructorStandings = "constructor_standings.csv"
    constructors = "constructors.csv"
    driverStandings = "driver_standings.csv"
    drivers = "drivers.csv"
    lapTimes = "lap_times.csv"
    pitStops = "pit_stops.csv"
    qualifying = "qualifying.csv"
    races = "races.csv"
    results = "results.csv"
    seasons = "seasons.csv"
    sprintResults = "sprint_results.csv"
    status = "status.csv"


class DashboardPlot(Enum):
    topPitStopDrivers = "topPitStopDrivers"
    averagePitStopTimeByYear = "averagePitStopTimeByYear"
    gridVersusFinish = "gridVersusFinish"
    topWinningDrivers = "topWinningDrivers"
    dnfRateByYear = "dnfRateByYear"
    circuitsPerCountry = "circuitsPerCountry"
    driverChampionshipMarginByYear = "driverChampionshipMarginByYear"
    constructorChampionsTimeline = "constructorChampionsTimeline"
    qualifyingPositionVersusGridPosition = "qualifyingPositionVersusGridPosition"
    sprintPointsShareByYear = "sprintPointsShareByYear"
    qualifyingPositionVersusFinishPosition = "qualifyingPositionVersusFinishPosition"
    constructorChampionshipMarginByYear = "constructorChampionshipMarginByYear"


@dataclass(frozen=True)
class DatasetConfig:
    datasetIdentifier: str
    missingValueTokenPattern: str
    localFallbackDirectory: Path


@dataclass(frozen=True)
class DashboardConfig:
    figureSize: Tuple[int, int]
    subplotRows: int
    subplotColumns: int
    pitStopTopCount: int
    winningDriversTopCount: int
    gridVersusFinishSampleSize: int
    circuitsCountryTopCount: int
    minimumResultsPerYearForDnfRate: int
    qualifyingVersusGridSampleSize: int
    qualifyingVersusFinishSampleSize: int
    minimumRowsPerYearForChampionshipMargin: int
    selectedPlots: Tuple[DashboardPlot, ...]


@dataclass(frozen=True)
class LoadedTableRegistry:
    tableDataFrames: Mapping[CsvTable, pd.DataFrame]

    def hasTable(self, csvTable: CsvTable) -> bool:
        return csvTable in self.tableDataFrames

    def getTable(self, csvTable: CsvTable) -> pd.DataFrame:
        return self.tableDataFrames[csvTable]

    def getAvailableTables(self) -> FrozenSet[CsvTable]:
        return frozenset(self.tableDataFrames.keys())


PlotFunction = Callable[[LoadedTableRegistry, DashboardConfig, Axes], None]


@dataclass(frozen=True)
class PlotSpec:
    plotType: DashboardPlot
    title: str
    requiredTables: FrozenSet[CsvTable]
    plotFunction: PlotFunction


def downloadDataset(datasetConfig: DatasetConfig) -> Path:
    datasetPath: Path = Path(kagglehub.dataset_download(datasetConfig.datasetIdentifier))
    return datasetPath


def getExistingCsvPath(datasetPath: Path, datasetConfig: DatasetConfig, csvTable: CsvTable) -> Optional[Path]:
    primaryPath: Path = datasetPath / csvTable.value
    if primaryPath.exists():
        return primaryPath
    fallbackPath: Path = datasetConfig.localFallbackDirectory / csvTable.value
    if fallbackPath.exists():
        return fallbackPath
    return None


def readCsv(datasetPath: Path, datasetConfig: DatasetConfig, csvTable: CsvTable) -> pd.DataFrame:
    existingPath: Optional[Path] = getExistingCsvPath(datasetPath, datasetConfig, csvTable)
    if existingPath is None:
        raise FileNotFoundError(csvTable.value)
    dataFrame: pd.DataFrame = pd.read_csv(existingPath)
    dataFrame = dataFrame.replace(datasetConfig.missingValueTokenPattern, np.nan, regex=True)
    return dataFrame


def printFiles(datasetPath: Path) -> None:
    fileNameList: List[str] = sorted([filePath.name for filePath in datasetPath.iterdir() if filePath.is_file()])
    print(f"Total number of files downloaded | {len(fileNameList)}")
    for index, fileName in enumerate(fileNameList, start=1):
        print(f"{index: >2} | {fileName}")


def convertNumericColumns(tableDataFrames: Dict[CsvTable, pd.DataFrame]) -> Dict[CsvTable, pd.DataFrame]:
    numericColumnRegistry: Mapping[CsvTable, Tuple[str, ...]] = {
        CsvTable.races: ("year", "round"),
        CsvTable.results: ("position", "positionOrder", "grid", "points"),
        CsvTable.pitStops: ("milliseconds",),
        CsvTable.driverStandings: ("points", "position"),
        CsvTable.constructorStandings: ("points", "position"),
        CsvTable.qualifying: ("position",),
        CsvTable.sprintResults: ("points", "position"),
        CsvTable.constructorResults: ("points",),
        CsvTable.seasons: ("year",),
        CsvTable.lapTimes: ("lap", "position", "milliseconds"),
    }

    for csvTable, columnNameTuple in numericColumnRegistry.items():
        if csvTable not in tableDataFrames:
            continue

        dataFrame: pd.DataFrame = tableDataFrames[csvTable]

        for columnName in columnNameTuple:
            if columnName in dataFrame.columns:
                dataFrame[columnName] = pd.to_numeric(dataFrame[columnName], errors="coerce")

        tableDataFrames[csvTable] = dataFrame

    return tableDataFrames


def loadTableRegistry(datasetPath: Path, datasetConfig: DatasetConfig) -> LoadedTableRegistry:
    tableDataFrames: Dict[CsvTable, pd.DataFrame] = {}
    for csvTable in CsvTable:
        existingPath: Optional[Path] = getExistingCsvPath(datasetPath, datasetConfig, csvTable)
        if existingPath is None:
            continue

        tableDataFrames[csvTable] = readCsv(datasetPath, datasetConfig, csvTable)

    tableDataFrames = convertNumericColumns(tableDataFrames)

    return LoadedTableRegistry(tableDataFrames=tableDataFrames)


def getDriverNameByDriverId(driversDataFrame: pd.DataFrame, driverIdentifier: int) -> str:
    matchedRows: pd.DataFrame = driversDataFrame[driversDataFrame["driverId"] == driverIdentifier]
    if matchedRows.empty:
        return str(driverIdentifier)
    
    forenameValue: str = str(matchedRows["forename"].iloc[0])
    surnameValue: str = str(matchedRows["surname"].iloc[0])
    driverName: str = (forenameValue + " " + surnameValue).strip()
    return driverName


def getConstructorNameByConstructorId(constructorsDataFrame: pd.DataFrame, constructorIdentifier: int) -> str:
    matchedRows: pd.DataFrame = constructorsDataFrame[constructorsDataFrame["constructorId"] == constructorIdentifier]
    if matchedRows.empty:
        return str(constructorIdentifier)
    
    if "name" in matchedRows.columns:
        return str(matchedRows["name"].iloc[0])
    
    if "constructorRef" in matchedRows.columns:
        return str(matchedRows["constructorRef"].iloc[0])
    
    return str(constructorIdentifier)


def getFinalRaceIdsByYear(racesDataFrame: pd.DataFrame) -> pd.DataFrame:
    if "raceId" not in racesDataFrame.columns or "year" not in racesDataFrame.columns or "round" not in racesDataFrame.columns:
        return pd.DataFrame(columns=["year", "raceId"])

    racesSubsetDataFrame: pd.DataFrame = racesDataFrame[["raceId", "year", "round"]].dropna(subset=["raceId", "year", "round"]).copy()
    racesSubsetDataFrame["round"] = pd.to_numeric(racesSubsetDataFrame["round"], errors="coerce")
    racesSubsetDataFrame = racesSubsetDataFrame.dropna(subset=["round"])

    finalRoundDataFrame: pd.DataFrame = racesSubsetDataFrame.groupby("year", as_index=False)["round"].max()
    finalRaceIdDataFrame: pd.DataFrame = racesSubsetDataFrame.merge(finalRoundDataFrame, on=["year", "round"], how="inner")
    finalRaceIdDataFrame = finalRaceIdDataFrame[["year", "raceId"]].drop_duplicates(subset=["year"])
    return finalRaceIdDataFrame


def plotTopPitStopDrivers(tableRegistry: LoadedTableRegistry, dashboardConfig: DashboardConfig, targetAxis: Axes) -> None:
    pitStopsDataFrame: pd.DataFrame = tableRegistry.getTable(CsvTable.pitStops)
    driversDataFrame: pd.DataFrame = tableRegistry.getTable(CsvTable.drivers)

    pitStopCounts: pd.Series = pitStopsDataFrame["driverId"].value_counts().head(dashboardConfig.pitStopTopCount)

    driverNameList: List[str] = []

    for driverIdentifierValue in pitStopCounts.index:
        driverNameList.append(getDriverNameByDriverId(driversDataFrame, int(driverIdentifierValue)))

    sortedIndexes: np.ndarray = np.argsort(pitStopCounts.values)

    targetAxis.barh(np.array(driverNameList)[sortedIndexes], pitStopCounts.values[sortedIndexes])
    targetAxis.set_title(f"Most pit stops (top {dashboardConfig.pitStopTopCount})")
    targetAxis.set_xlabel("Pit stops")


def plotAveragePitStopTimeByYear(tableRegistry: LoadedTableRegistry, dashboardConfig: DashboardConfig, targetAxis: Axes) -> None:
    pitStopsDataFrame: pd.DataFrame = tableRegistry.getTable(CsvTable.pitStops)
    racesDataFrame: pd.DataFrame = tableRegistry.getTable(CsvTable.races)

    mergedDataFrame: pd.DataFrame = pitStopsDataFrame.merge(racesDataFrame[["raceId", "year"]], on="raceId", how="left")
    filteredDataFrame: pd.DataFrame = mergedDataFrame.dropna(subset=["year", "milliseconds"])
    yearlyAverageDataFrame: pd.DataFrame = filteredDataFrame.groupby("year", as_index=False)["milliseconds"].mean()

    targetAxis.plot(yearlyAverageDataFrame["year"], yearlyAverageDataFrame["milliseconds"])
    targetAxis.set_title("Average pit stop time by year")
    targetAxis.set_xlabel("Year")
    targetAxis.set_ylabel("Milliseconds")


def plotGridVersusFinish(tableRegistry: LoadedTableRegistry, dashboardConfig: DashboardConfig, targetAxis: Axes) -> None:
    resultsDataFrame: pd.DataFrame = tableRegistry.getTable(CsvTable.results)

    filteredDataFrame: pd.DataFrame = resultsDataFrame.dropna(subset=["grid", "positionOrder"]).copy()
    filteredDataFrame = filteredDataFrame[(filteredDataFrame["grid"] > 0) & (filteredDataFrame["positionOrder"] > 0)]

    if len(filteredDataFrame) > dashboardConfig.gridVersusFinishSampleSize:
        filteredDataFrame = filteredDataFrame.sample(dashboardConfig.gridVersusFinishSampleSize, random_state=42)

    maximumValue: int = int(max(filteredDataFrame["grid"].max(), filteredDataFrame["positionOrder"].max()))

    targetAxis.scatter(filteredDataFrame["grid"], filteredDataFrame["positionOrder"], s=5, alpha=0.3)
    targetAxis.plot([1, maximumValue], [1, maximumValue])
    targetAxis.set_title("Grid position vs finish position")
    targetAxis.set_xlabel("Grid position")
    targetAxis.set_ylabel("Finish position")


def plotTopWinningDrivers(tableRegistry: LoadedTableRegistry, dashboardConfig: DashboardConfig, targetAxis: Axes) -> None:
    resultsDataFrame: pd.DataFrame = tableRegistry.getTable(CsvTable.results)
    driversDataFrame: pd.DataFrame = tableRegistry.getTable(CsvTable.drivers)

    winnersDataFrame: pd.DataFrame = resultsDataFrame[resultsDataFrame["position"] == 1].merge(
        driversDataFrame[["driverId", "forename", "surname"]], on="driverId", how="left")

    winnersDataFrame["driverName"] = winnersDataFrame["forename"].fillna("").astype(str) + " " + winnersDataFrame["surname"].fillna("").astype(str)
    winCounts: pd.Series = winnersDataFrame["driverName"].value_counts().head(dashboardConfig.winningDriversTopCount).sort_values()

    targetAxis.barh(winCounts.index, winCounts.values)
    targetAxis.set_title(f"Most wins (top {dashboardConfig.winningDriversTopCount})")
    targetAxis.set_xlabel("Wins")


def plotDnfRateByYear(tableRegistry: LoadedTableRegistry, dashboardConfig: DashboardConfig, targetAxis: Axes) -> None:
    resultsDataFrame: pd.DataFrame = tableRegistry.getTable(CsvTable.results)
    racesDataFrame: pd.DataFrame = tableRegistry.getTable(CsvTable.races)
    statusDataFrame: pd.DataFrame = tableRegistry.getTable(CsvTable.status)

    mergedDataFrame: pd.DataFrame = resultsDataFrame.merge(racesDataFrame[["raceId", "year"]], on="raceId", how="left").merge(
        statusDataFrame[["statusId", "status"]], on="statusId", how="left")

    filteredDataFrame: pd.DataFrame = mergedDataFrame.dropna(subset=["year", "status"]).copy()
    filteredDataFrame["isDnf"] = filteredDataFrame["status"].ne("Finished")

    yearlyRateDataFrame: pd.DataFrame = filteredDataFrame.groupby("year", as_index=False).agg(dnfRate=("isDnf", "mean"), resultCount=("isDnf", "size"))

    yearlyRateDataFrame = yearlyRateDataFrame[yearlyRateDataFrame["resultCount"] >= dashboardConfig.minimumResultsPerYearForDnfRate]

    targetAxis.plot(yearlyRateDataFrame["year"], yearlyRateDataFrame["dnfRate"] * 100.0)
    targetAxis.set_title("DNF rate by year")
    targetAxis.set_xlabel("Year")
    targetAxis.set_ylabel("DNF rate (%)")


def plotCircuitsPerCountry(tableRegistry: LoadedTableRegistry, dashboardConfig: DashboardConfig, targetAxis: Axes) -> None:
    circuitsDataFrame: pd.DataFrame = tableRegistry.getTable(CsvTable.circuits)

    if "country" not in circuitsDataFrame.columns:
        targetAxis.set_visible(False)
        return

    countryCounts: pd.Series = circuitsDataFrame["country"].value_counts().head(dashboardConfig.circuitsCountryTopCount).sort_values()
    targetAxis.barh(countryCounts.index, countryCounts.values)
    targetAxis.set_title(f"Circuits by country (top {dashboardConfig.circuitsCountryTopCount})")
    targetAxis.set_xlabel("Circuit count")


def plotDriverChampionshipMarginByYear(tableRegistry: LoadedTableRegistry, dashboardConfig: DashboardConfig, targetAxis: Axes) -> None:
    racesDataFrame: pd.DataFrame = tableRegistry.getTable(CsvTable.races)
    driverStandingsDataFrame: pd.DataFrame = tableRegistry.getTable(CsvTable.driverStandings)

    finalRaceIdDataFrame: pd.DataFrame = getFinalRaceIdsByYear(racesDataFrame)
    
    if finalRaceIdDataFrame.empty:
        targetAxis.set_visible(False)
        return

    finalStandingsDataFrame: pd.DataFrame = driverStandingsDataFrame.merge(finalRaceIdDataFrame, on="raceId", how="inner")
    finalStandingsDataFrame = finalStandingsDataFrame.dropna(subset=["year", "position", "points"]).copy()
    finalStandingsDataFrame = finalStandingsDataFrame[finalStandingsDataFrame["position"].isin([1, 2])]

    if finalStandingsDataFrame.empty:
        targetAxis.set_visible(False)
        return

    pivotDataFrame: pd.DataFrame = finalStandingsDataFrame.pivot_table(index="year", columns="position", values="points", aggfunc="max").reset_index()
    pivotDataFrame = pivotDataFrame.dropna(subset=[1, 2]).copy()
    pivotDataFrame["marginPoints"] = pivotDataFrame[1] - pivotDataFrame[2]

    rowCountDataFrame: pd.DataFrame = finalStandingsDataFrame.groupby("year", as_index=False).size().rename(columns={"size": "standingRows"})
    pivotDataFrame = pivotDataFrame.merge(rowCountDataFrame, on="year", how="left")
    pivotDataFrame = pivotDataFrame[pivotDataFrame["standingRows"] >= dashboardConfig.minimumRowsPerYearForChampionshipMargin]

    targetAxis.plot(pivotDataFrame["year"], pivotDataFrame["marginPoints"])
    targetAxis.set_title("Driver title margin (P1 - P2)")
    targetAxis.set_xlabel("Year")
    targetAxis.set_ylabel("Points")


def plotConstructorChampionsTimeline(tableRegistry: LoadedTableRegistry, dashboardConfig: DashboardConfig, targetAxis: Axes) -> None:
    racesDataFrame: pd.DataFrame = tableRegistry.getTable(CsvTable.races)
    constructorStandingsDataFrame: pd.DataFrame = tableRegistry.getTable(CsvTable.constructorStandings)
    constructorsDataFrame: pd.DataFrame = tableRegistry.getTable(CsvTable.constructors)

    finalRaceIdDataFrame: pd.DataFrame = getFinalRaceIdsByYear(racesDataFrame)
    
    if finalRaceIdDataFrame.empty:
        targetAxis.set_visible(False)
        return

    finalStandingsDataFrame: pd.DataFrame = constructorStandingsDataFrame.merge(finalRaceIdDataFrame, on="raceId", how="inner")
    finalStandingsDataFrame = finalStandingsDataFrame.dropna(subset=["year", "position", "constructorId"]).copy()
    championRowsDataFrame: pd.DataFrame = finalStandingsDataFrame[finalStandingsDataFrame["position"] == 1][["year", "constructorId"]].copy()

    if championRowsDataFrame.empty:
        targetAxis.set_visible(False)
        return

    championRowsDataFrame["constructorName"] = championRowsDataFrame["constructorId"].astype(int).apply(
        lambda constructorIdentifier: getConstructorNameByConstructorId(constructorsDataFrame, constructorIdentifier))

    constructorNameList: List[str] = list(dict.fromkeys(championRowsDataFrame["constructorName"].tolist()))
    constructorNameToIndex: Dict[str, int] = {constructorName: index for index, constructorName in enumerate(constructorNameList)}
    championRowsDataFrame["constructorIndex"] = championRowsDataFrame["constructorName"].map(constructorNameToIndex)

    targetAxis.scatter(championRowsDataFrame["year"], championRowsDataFrame["constructorIndex"], s=25)
    targetAxis.set_title("Constructor champions timeline")
    targetAxis.set_xlabel("Year")
    targetAxis.set_yticks(list(constructorNameToIndex.values()))
    targetAxis.set_yticklabels(list(constructorNameToIndex.keys()))


def plotQualifyingPositionVersusGridPosition(tableRegistry: LoadedTableRegistry, dashboardConfig: DashboardConfig, targetAxis: Axes) -> None:
    qualifyingDataFrame: pd.DataFrame = tableRegistry.getTable(CsvTable.qualifying)
    resultsDataFrame: pd.DataFrame = tableRegistry.getTable(CsvTable.results)

    qualifyingSubsetDataFrame: pd.DataFrame = qualifyingDataFrame.dropna(subset=["raceId", "driverId", "position"]).copy()
    resultsSubsetDataFrame: pd.DataFrame = resultsDataFrame.dropna(subset=["raceId", "driverId", "grid"]).copy()

    mergedDataFrame: pd.DataFrame = qualifyingSubsetDataFrame.merge(
        resultsSubsetDataFrame[["raceId", "driverId", "grid"]], on=["raceId", "driverId"], how="inner").dropna(subset=["position", "grid"])

    mergedDataFrame = mergedDataFrame[(mergedDataFrame["position"] > 0) & (mergedDataFrame["grid"] > 0)]

    if mergedDataFrame.empty:
        targetAxis.set_visible(False)
        return

    if len(mergedDataFrame) > dashboardConfig.qualifyingVersusGridSampleSize:
        mergedDataFrame = mergedDataFrame.sample(dashboardConfig.qualifyingVersusGridSampleSize, random_state=42)

    maximumValue: int = int(max(mergedDataFrame["position"].max(), mergedDataFrame["grid"].max()))

    targetAxis.scatter(mergedDataFrame["position"], mergedDataFrame["grid"], s=5, alpha=0.3)
    targetAxis.plot([1, maximumValue], [1, maximumValue])
    targetAxis.set_title("Qualifying position vs grid position")
    targetAxis.set_xlabel("Qualifying position")
    targetAxis.set_ylabel("Grid position")


def plotSprintPointsShareByYear(tableRegistry: LoadedTableRegistry, dashboardConfig: DashboardConfig, targetAxis: Axes) -> None:
    sprintResultsDataFrame: pd.DataFrame = tableRegistry.getTable(CsvTable.sprintResults)
    resultsDataFrame: pd.DataFrame = tableRegistry.getTable(CsvTable.results)
    racesDataFrame: pd.DataFrame = tableRegistry.getTable(CsvTable.races)

    sprintPointsDataFrame: pd.DataFrame = sprintResultsDataFrame.merge(racesDataFrame[["raceId", "year"]], on="raceId", how="left").dropna(subset=["year", "points"])
    racePointsDataFrame: pd.DataFrame = resultsDataFrame.merge(racesDataFrame[["raceId", "year"]], on="raceId", how="left").dropna(subset=["year", "points"])

    sprintByYearDataFrame: pd.DataFrame = sprintPointsDataFrame.groupby("year", as_index=False)["points"].sum().rename(columns={"points": "sprintPoints"})
    raceByYearDataFrame: pd.DataFrame = racePointsDataFrame.groupby("year", as_index=False)["points"].sum().rename(columns={"points": "racePoints"})

    mergedByYearDataFrame: pd.DataFrame = raceByYearDataFrame.merge(sprintByYearDataFrame, on="year", how="left")
    mergedByYearDataFrame["sprintPoints"] = mergedByYearDataFrame["sprintPoints"].fillna(0.0)
    mergedByYearDataFrame["totalPoints"] = mergedByYearDataFrame["racePoints"] + mergedByYearDataFrame["sprintPoints"]
    mergedByYearDataFrame = mergedByYearDataFrame[mergedByYearDataFrame["totalPoints"] > 0]
    mergedByYearDataFrame["sprintSharePercent"] = (mergedByYearDataFrame["sprintPoints"] / mergedByYearDataFrame["totalPoints"]) * 100.0

    targetAxis.plot(mergedByYearDataFrame["year"], mergedByYearDataFrame["sprintSharePercent"])
    targetAxis.set_title("Sprint points share by year")
    targetAxis.set_xlabel("Year")
    targetAxis.set_ylabel("Sprint share (%)")


def plotQualifyingPositionVersusFinishPosition(tableRegistry: LoadedTableRegistry, dashboardConfig: DashboardConfig, targetAxis: Axes) -> None:
    qualifyingDataFrame: pd.DataFrame = tableRegistry.getTable(CsvTable.qualifying)
    resultsDataFrame: pd.DataFrame = tableRegistry.getTable(CsvTable.results)

    qualifyingSubsetDataFrame: pd.DataFrame = qualifyingDataFrame.dropna(subset=["raceId", "driverId", "position"]).copy()
    resultsSubsetDataFrame: pd.DataFrame = resultsDataFrame.dropna(subset=["raceId", "driverId", "positionOrder"]).copy()

    mergedDataFrame: pd.DataFrame = qualifyingSubsetDataFrame.merge(
        resultsSubsetDataFrame[["raceId", "driverId", "positionOrder"]], on=["raceId", "driverId"], how="inner").dropna(subset=["position", "positionOrder"])

    mergedDataFrame = mergedDataFrame[(mergedDataFrame["position"] > 0) & (mergedDataFrame["positionOrder"] > 0)]

    if mergedDataFrame.empty:
        targetAxis.set_visible(False)
        return

    if len(mergedDataFrame) > dashboardConfig.qualifyingVersusFinishSampleSize:
        mergedDataFrame = mergedDataFrame.sample(dashboardConfig.qualifyingVersusFinishSampleSize, random_state=42)

    maximumValue: int = int(max(mergedDataFrame["position"].max(), mergedDataFrame["positionOrder"].max()))

    targetAxis.scatter(mergedDataFrame["position"], mergedDataFrame["positionOrder"], s=5, alpha=0.3)
    targetAxis.plot([1, maximumValue], [1, maximumValue])
    targetAxis.set_title("Qualifying position vs finish position")
    targetAxis.set_xlabel("Qualifying position")
    targetAxis.set_ylabel("Finish position")


def plotConstructorChampionshipMarginByYear(tableRegistry: LoadedTableRegistry, dashboardConfig: DashboardConfig, targetAxis: Axes) -> None:
    racesDataFrame: pd.DataFrame = tableRegistry.getTable(CsvTable.races)
    constructorStandingsDataFrame: pd.DataFrame = tableRegistry.getTable(CsvTable.constructorStandings)

    finalRaceIdDataFrame: pd.DataFrame = getFinalRaceIdsByYear(racesDataFrame)
    if finalRaceIdDataFrame.empty:
        targetAxis.set_visible(False)
        return

    finalStandingsDataFrame: pd.DataFrame = constructorStandingsDataFrame.merge(finalRaceIdDataFrame, on="raceId", how="inner")
    finalStandingsDataFrame = finalStandingsDataFrame.dropna(subset=["year", "position", "points"]).copy()
    finalStandingsDataFrame = finalStandingsDataFrame[finalStandingsDataFrame["position"].isin([1, 2])]

    if finalStandingsDataFrame.empty:
        targetAxis.set_visible(False)
        return

    pivotDataFrame: pd.DataFrame = finalStandingsDataFrame.pivot_table(index="year", columns="position", values="points", aggfunc="max").reset_index()
    pivotDataFrame = pivotDataFrame.dropna(subset=[1, 2]).copy()
    pivotDataFrame["marginPoints"] = pivotDataFrame[1] - pivotDataFrame[2]

    rowCountDataFrame: pd.DataFrame = finalStandingsDataFrame.groupby("year", as_index=False).size().rename(columns={"size": "standingRows"})
    pivotDataFrame = pivotDataFrame.merge(rowCountDataFrame, on="year", how="left")
    pivotDataFrame = pivotDataFrame[pivotDataFrame["standingRows"] >= dashboardConfig.minimumRowsPerYearForChampionshipMargin]

    targetAxis.plot(pivotDataFrame["year"], pivotDataFrame["marginPoints"])
    targetAxis.set_title("Constructor title margin (P1 - P2)")
    targetAxis.set_xlabel("Year")
    targetAxis.set_ylabel("Points")


def getPlotSpecs() -> Dict[DashboardPlot, PlotSpec]:
    plotSpecList: List[PlotSpec] = [
        PlotSpec(plotType=DashboardPlot.topPitStopDrivers, title="Most pit stops", requiredTables=frozenset({CsvTable.drivers, CsvTable.pitStops}), plotFunction=plotTopPitStopDrivers),
        PlotSpec(plotType=DashboardPlot.averagePitStopTimeByYear, title="Average pit stop time by year", requiredTables=frozenset({CsvTable.races, CsvTable.pitStops}), plotFunction=plotAveragePitStopTimeByYear),
        PlotSpec(plotType=DashboardPlot.gridVersusFinish, title="Grid vs finish", requiredTables=frozenset({CsvTable.results}), plotFunction=plotGridVersusFinish),
        PlotSpec(plotType=DashboardPlot.topWinningDrivers, title="Most wins", requiredTables=frozenset({CsvTable.drivers, CsvTable.results}), plotFunction=plotTopWinningDrivers),
        PlotSpec(plotType=DashboardPlot.dnfRateByYear, title="DNF rate by year", requiredTables=frozenset({CsvTable.races, CsvTable.results, CsvTable.status}), plotFunction=plotDnfRateByYear),
        PlotSpec(plotType=DashboardPlot.circuitsPerCountry, title="Circuits by country", requiredTables=frozenset({CsvTable.circuits}), plotFunction=plotCircuitsPerCountry),
        PlotSpec(plotType=DashboardPlot.driverChampionshipMarginByYear, title="Driver title margin", requiredTables=frozenset({CsvTable.races, CsvTable.driverStandings}), plotFunction=plotDriverChampionshipMarginByYear),
        PlotSpec(plotType=DashboardPlot.constructorChampionsTimeline, title="Constructor champions timeline", requiredTables=frozenset({CsvTable.races, CsvTable.constructorStandings, CsvTable.constructors}), plotFunction=plotConstructorChampionsTimeline),
        PlotSpec(plotType=DashboardPlot.qualifyingPositionVersusGridPosition, title="Qualifying vs grid", requiredTables=frozenset({CsvTable.qualifying, CsvTable.results}), plotFunction=plotQualifyingPositionVersusGridPosition),
        PlotSpec(plotType=DashboardPlot.sprintPointsShareByYear, title="Sprint points share", requiredTables=frozenset({CsvTable.sprintResults, CsvTable.results, CsvTable.races}), plotFunction=plotSprintPointsShareByYear),
        PlotSpec(plotType=DashboardPlot.qualifyingPositionVersusFinishPosition, title="Qualifying vs finish", requiredTables=frozenset({CsvTable.qualifying, CsvTable.results}), plotFunction=plotQualifyingPositionVersusFinishPosition),
        PlotSpec(plotType=DashboardPlot.constructorChampionshipMarginByYear, title="Constructor title margin", requiredTables=frozenset({CsvTable.races, CsvTable.constructorStandings}), plotFunction=plotConstructorChampionshipMarginByYear),
    ]

    plotSpecRegistry: Dict[DashboardPlot, PlotSpec] = {}
    for plotSpec in plotSpecList:
        plotSpecRegistry[plotSpec.plotType] = plotSpec
    return plotSpecRegistry


def validateSelectedPlots(plotSpecRegistry: Mapping[DashboardPlot, PlotSpec], selectedPlots: Sequence[DashboardPlot], availableTables: FrozenSet[CsvTable]) -> List[DashboardPlot]:
    validPlotList: List[DashboardPlot] = []
    for plotType in selectedPlots:
        if plotType not in plotSpecRegistry:
            continue

        plotSpec: PlotSpec = plotSpecRegistry[plotType]

        if plotSpec.requiredTables.issubset(availableTables):
            validPlotList.append(plotType)

    return validPlotList


def toAxisList(axisGrid: np.ndarray) -> List[Axes]:
    axisList: List[Axes] = []
    for axisValue in axisGrid.ravel():
        axisList.append(axisValue)
    return axisList


def plotDashboard(tableRegistry: LoadedTableRegistry, dashboardConfig: DashboardConfig) -> None:
    plotSpecRegistry: Dict[DashboardPlot, PlotSpec] = getPlotSpecs()
    availableTables: FrozenSet[CsvTable] = tableRegistry.getAvailableTables()
    selectedPlotList: List[DashboardPlot] = validateSelectedPlots(plotSpecRegistry, dashboardConfig.selectedPlots, availableTables)

    figure: Figure
    axisGrid: np.ndarray
    figure, axisGrid = plot.subplots(dashboardConfig.subplotRows, dashboardConfig.subplotColumns, figsize=dashboardConfig.figureSize)

    axisList: List[Axes] = toAxisList(axisGrid)
    selectedPlotCount: int = min(len(selectedPlotList), len(axisList))

    for index in range(selectedPlotCount):
        plotType: DashboardPlot = selectedPlotList[index]
        plotSpec: PlotSpec = plotSpecRegistry[plotType]
        plotSpec.plotFunction(tableRegistry, dashboardConfig, axisList[index])

    for index in range(selectedPlotCount, len(axisList)):
        axisList[index].set_visible(False)

    figure.suptitle("F1 Dataset Dashboard", fontsize=16)
    figure.tight_layout()
    plot.show()


def main(devMode: bool) -> None:
    datasetConfig: DatasetConfig = DatasetConfig(datasetIdentifier="rohanrao/formula-1-world-championship-1950-2020", missingValueTokenPattern=r"\\N", localFallbackDirectory=Path("/mnt/data"))

    dashboardConfig: DashboardConfig = DashboardConfig(
        figureSize=(22, 12),
        subplotRows=3,
        subplotColumns=4,
        pitStopTopCount=15,
        winningDriversTopCount=10,
        gridVersusFinishSampleSize=30000,
        circuitsCountryTopCount=15,
        minimumResultsPerYearForDnfRate=100,
        qualifyingVersusGridSampleSize=35000,
        qualifyingVersusFinishSampleSize=35000,
        minimumRowsPerYearForChampionshipMargin=2,
        selectedPlots=(
            DashboardPlot.topPitStopDrivers,
            DashboardPlot.averagePitStopTimeByYear,
            DashboardPlot.gridVersusFinish,
            DashboardPlot.topWinningDrivers,
            DashboardPlot.dnfRateByYear,
            DashboardPlot.circuitsPerCountry,
            DashboardPlot.driverChampionshipMarginByYear,
            DashboardPlot.constructorChampionsTimeline,
            DashboardPlot.qualifyingPositionVersusGridPosition,
            DashboardPlot.qualifyingPositionVersusFinishPosition,
            DashboardPlot.sprintPointsShareByYear,
            DashboardPlot.constructorChampionshipMarginByYear,
        )
    )

    datasetPath: Path = downloadDataset(datasetConfig)
    printFiles(datasetPath)

    tableRegistry: LoadedTableRegistry = loadTableRegistry(datasetPath, datasetConfig)
    plotDashboard(tableRegistry, dashboardConfig)

    if devMode:
        print(datasetPath)
        print(f"Loaded tables: {sorted([table.value for table in tableRegistry.getAvailableTables()])}")


if __name__ == "__main__":
    try:
        main(True)
    except KeyboardInterrupt:
        print("Bye :(")
