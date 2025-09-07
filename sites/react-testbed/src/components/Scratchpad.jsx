const Scratchpad = () => {
    return (
        <div>
            <label htmlFor="scratchpad">Scratchpad</label>
            <textarea
                id="scratchpad"
                placeholder="Scratchpad"
                aria-label="Scratchpad"
                style={{
                    position: "fixed",
                    bottom: 20,
                    right: 20,
                    width: 200,
                    height: 100,
                    pointerEvents: "auto",
                    background: "rgba(255,255,255,0.8)",
                    color: "#000",
                    border: "1px solid #ccc",
                    zIndex: 1000, // Ensure it's on top
                }}
            />
        </div>
    );
}

export default Scratchpad;