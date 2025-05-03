operation MachZehnder() : Result {
    // allocate a new qubit in default state
    use photon = Qubit();

    // beam splitter
    H(photon);

    // second beam splitter
    H(photon);

    // result is a certain Zero ("detector2") due to interference
    return MResetZ(photon);
}

operation MachZehnderWithQND() : (Result, Result) {
    // allocate a new qubit in default state
    use photon = Qubit();

    // beam splitter
    H(photon);

    // observe using the QND - it is a random Zero or One (so a random blip on QND 1 or QND 2)
    let qndResult = MResetZ(photon);

    // second beam splitter
    H(photon);

    // result is now random Zero or One ("detector1" or "detector2" - interference disappears
    let detectorResult = MResetZ(photon);

    return (qndResult, detectorResult);
}