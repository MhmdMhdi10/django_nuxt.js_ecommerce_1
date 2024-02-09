import React, { useState, useEffect } from 'react';

const Carousel = ({ items, options }) => {
    const [currentPosition, setCurrentPosition] = useState(options.defaultPosition || 0);

    useEffect(() => {
        const intervalId = setInterval(() => {
            handleNext();
        }, options.interval || 3000);

        return () => {
            clearInterval(intervalId);
        };
    }, []);

    const handleNext = () => {
        const nextPosition = (currentPosition + 1) % items.length;
        setCurrentPosition(nextPosition);
        if (options.onNext) {
            options.onNext(nextPosition);
        }
    };

    const handlePrev = () => {
        const prevPosition = currentPosition === 0 ? items.length - 1 : currentPosition - 1;
        setCurrentPosition(prevPosition);
        if (options.onPrev) {
            options.onPrev(prevPosition);
        }
    };

    const handleIndicatorClick = (position) => {
        setCurrentPosition(position);
        if (options.onChange) {
            options.onChange(position);
        }
    };

    return (
        <div className="carousel">
            <div className="carousel-items">
                {items.map((item, index) => (
                    <div
                        key={index}
                        className={`carousel-item ${currentPosition === index ? 'active' : ''}`}
                    >
                        {item.el}
                    </div>
                ))}
            </div>
            {options.indicators && (
                <div className="carousel-indicators">
                    {options.indicators.items.map((indicator, index) => (
                        <div
                            key={index}
                            className={`carousel-indicator ${
                                currentPosition === indicator.position ? options.indicators.activeClasses : options.indicators.inactiveClasses
                            }`}
                            onClick={() => handleIndicatorClick(indicator.position)}
                        ></div>
                    ))}
                </div>
            )}
            <button className="carousel-prev" onClick={handlePrev}>
                Previous
            </button>
            <button className="carousel-next" onClick={handleNext}>
                Next
            </button>
        </div>
    );
};

export default Carousel;
